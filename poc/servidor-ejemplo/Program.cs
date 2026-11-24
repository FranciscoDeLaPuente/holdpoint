using System.ComponentModel;
using ModelContextProtocol.Server;

var builder = WebApplication.CreateBuilder(args);
builder.WebHost.UseUrls("http://127.0.0.1:5100");
builder.Services.AddMcpServer().WithHttpTransport().WithToolsFromAssembly();

var app = builder.Build();
app.MapMcp("/mcp");
app.Run();

[McpServerToolType]
public static class Tareas
{
    // Estado en memoria: basta para la prueba de concepto.
    private static readonly List<(int Id, string Titulo)> _tareas =
        [(1, "Preparar la demo"), (2, "Revisar el informe"), (3, "Llamar al proveedor")];
    private static readonly object _cerrojo = new();

    [McpServerTool(Name = "listar_tareas", ReadOnly = true), Description("Lista las tareas existentes")]
    public static string ListarTareas()
    {
        lock (_cerrojo) return string.Join("\n", _tareas.Select(t => $"{t.Id}: {t.Titulo}"));
    }

    [McpServerTool(Name = "borrar_tarea", Destructive = true), Description("Borra una tarea por su id")]
    public static string BorrarTarea([Description("Id de la tarea")] int id)
    {
        lock (_cerrojo)
        {
            var n = _tareas.RemoveAll(t => t.Id == id);
            return n == 0 ? $"No existe la tarea {id}" : $"Tarea {id} borrada";
        }
    }
}
