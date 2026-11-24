using System.Text.Json;
using ModelContextProtocol;
using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol;

var builder = WebApplication.CreateBuilder(args);
builder.WebHost.UseUrls("http://127.0.0.1:5200");

// P1: segundos entre notificaciones de progreso mientras se espera (0 = no enviar).
var intervaloProgreso = int.Parse(builder.Configuration["IntervaloProgreso"] ?? "0");
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
        // P2: capacidades que declara el cliente en initialize.
        Console.WriteLine($"[pasarela] cliente={JsonSerializer.Serialize(ctx.Server.ClientInfo)} capacidades={JsonSerializer.Serialize(ctx.Server.ClientCapabilities)}");
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
        // P1: ¿trae el tools/call un progressToken?
        var token = ctx.Params.ProgressToken;
        Console.WriteLine($"[pasarela] progressToken={(token is null ? "ninguno" : token.ToString())} meta={ctx.Params.Meta?.ToJsonString()}");
        var inicio = DateTime.UtcNow;
        try
        {
            var llamada = c.CallToolAsync(ctx.Params, ct).AsTask();
            var n = 0;
            while (intervaloProgreso > 0 && token is not null)
            {
                if (await Task.WhenAny(llamada, Task.Delay(TimeSpan.FromSeconds(intervaloProgreso), ct)) == llamada) break;
                n++;
                await ctx.Server.NotifyProgressAsync(token.Value, new ProgressNotificationValue { Progress = n, Message = "esperando" }, cancellationToken: ct);
                Console.WriteLine($"[pasarela] progreso #{n} enviado a los {(DateTime.UtcNow - inicio).TotalSeconds:F0} s");
            }
            var r = await llamada;
            Console.WriteLine($"[pasarela] resultado isError={r.IsError} a los {(DateTime.UtcNow - inicio).TotalSeconds:F1} s");
            return r;
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine($"[pasarela] CANCELADA por el cliente a los {(DateTime.UtcNow - inicio).TotalSeconds:F1} s");
            throw;
        }
    });

var app = builder.Build();
app.MapMcp("/mcp");
app.Run();
