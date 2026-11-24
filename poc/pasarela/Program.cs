using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol;

var builder = WebApplication.CreateBuilder(args);
builder.WebHost.UseUrls("http://127.0.0.1:5200");

var destino = builder.Configuration["Destino"] ?? "http://127.0.0.1:5100/mcp";

// Cliente hacia el servidor de ejemplo, creado una vez y compartido.
var cliente = new Lazy<Task<McpClient>>(() => McpClient.CreateAsync(
    // HttpClient.Timeout vale 100 s por defecto y cortaría las esperas largas (comprobación 5).
    new HttpClientTransport(
        new HttpClientTransportOptions { Endpoint = new Uri(destino), Name = "servidor-ejemplo" },
        new HttpClient { Timeout = Timeout.InfiniteTimeSpan },
        loggerFactory: null,
        ownsHttpClient: true)));

builder.Services.AddMcpServer()
    .WithHttpTransport()
    .WithListToolsHandler(async (ctx, ct) =>
    {
        var c = await cliente.Value;
        var tools = await c.ListToolsAsync(cancellationToken: ct);
        Console.WriteLine($"[pasarela] tools/list -> {tools.Count} herramientas");
        return new ListToolsResult { Tools = tools.Select(t => t.ProtocolTool).ToList() };
    })
    .WithCallToolHandler(async (ctx, ct) =>
    {
        // Política de la prueba de concepto: las herramientas destructivas se bloquean.
        if (ctx.Params!.Name == "borrar_tarea")
        {
            Console.WriteLine($"[pasarela] BLOQUEADA {ctx.Params.Name}");
            return new CallToolResult
            {
                IsError = true,
                Content = [new TextContentBlock { Text = "Bloqueada por política" }]
            };
        }
        var c = await cliente.Value;
        Console.WriteLine($"[pasarela] tools/call {ctx.Params!.Name} {System.Text.Json.JsonSerializer.Serialize(ctx.Params.Arguments)}");
        var r = await c.CallToolAsync(ctx.Params, ct);
        Console.WriteLine($"[pasarela] resultado isError={r.IsError}");
        return r;
    });

var app = builder.Build();
app.MapMcp("/mcp");
app.Run();
