using Prometheus;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOpenApi();

var app = builder.Build();

app.UseHttpMetrics();
app.MapMetrics("/metrics");

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

var items = new List<Item>
{
    new Item(1, "Item 1", "First item"),
    new Item(2, "Item 2", "Second item"),
    new Item(3, "Item 3", "Third item"),
};

app.MapGet("/api/health", () => Results.Json(new { status = "ok", message = "Server is running" }));

app.MapGet("/api/hello", (HttpRequest request) =>
{
    var name = request.Query["name"].ToString();
    if (string.IsNullOrWhiteSpace(name))
    {
        name = "World";
    }

    return Results.Json(new { message = $"Hello, {name}!" });
});

app.MapGet("/api/items", () => Results.Json(new { items }));

app.MapGet("/api/items/{id:int}", (int id) =>
{
    var item = items.FirstOrDefault(i => i.Id == id);
    return item is not null
        ? Results.Json(item)
        : Results.NotFound(new { error = "Item not found" });
});

app.MapPost("/api/items", async (HttpRequest request) =>
{
    var createItem = await request.ReadFromJsonAsync<CreateItem>();
    if (createItem is null || string.IsNullOrWhiteSpace(createItem.Name))
    {
        return Results.BadRequest(new { error = "Invalid request. \"name\" is required" });
    }

    var newId = items.Max(i => i.Id) + 1;
    var newItem = new Item(newId, createItem.Name.Trim(), createItem.Description ?? string.Empty);
    return Results.Created($"/api/items/{newItem.Id}", newItem);
});

app.Run("http://0.0.0.0:5000");

record Item(int Id, string Name, string Description);
record CreateItem(string Name, string? Description);
