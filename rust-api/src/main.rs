use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
struct HealthResponse {
    status: &'static str,
    message: &'static str,
}

#[derive(Serialize)]
struct MessageResponse {
    message: String,
}

#[derive(Serialize, Clone)]
struct Item {
    id: u32,
    name: String,
    description: String,
}

#[derive(Deserialize)]
struct CreateItem {
    name: String,
    description: Option<String>,
}

fn sample_items() -> Vec<Item> {
    vec![
        Item { id: 1, name: "Item 1".into(), description: "First item".into() },
        Item { id: 2, name: "Item 2".into(), description: "Second item".into() },
        Item { id: 3, name: "Item 3".into(), description: "Third item".into() },
    ]
}

#[get("/api/health")]
async fn health_check() -> impl Responder {
    HttpResponse::Ok().json(HealthResponse { status: "ok", message: "Server is running" })
}

#[derive(Deserialize, Default)]
struct HelloQuery {
    name: Option<String>,
}

#[get("/api/hello")]
async fn hello(query: web::Query<HelloQuery>) -> impl Responder {
    let name = query.name.clone().unwrap_or_else(|| "World".into());
    HttpResponse::Ok().json(MessageResponse { message: format!("Hello, {}!", name) })
}

#[get("/api/items")]
async fn get_items() -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "items": sample_items() }))
}

#[get("/api/items/{id}")]
async fn get_item(path: web::Path<u32>) -> impl Responder {
    let item_id = path.into_inner();
    match sample_items().into_iter().find(|item| item.id == item_id) {
        Some(item) => HttpResponse::Ok().json(item),
        None => HttpResponse::NotFound().json(serde_json::json!({ "error": "Item not found" })),
    }
}

#[post("/api/items")]
async fn create_item(payload: web::Json<CreateItem>) -> impl Responder {
    if payload.name.trim().is_empty() {
        return HttpResponse::BadRequest().json(serde_json::json!({ "error": "Invalid request. \"name\" is required" }));
    }

    let new_item = Item {
        id: 4,
        name: payload.name.clone(),
        description: payload.description.clone().unwrap_or_default(),
    };

    HttpResponse::Created().json(new_item)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("Starting Rust API on port 5000...");
    HttpServer::new(|| {
        App::new()
            .service(health_check)
            .service(hello)
            .service(get_items)
            .service(get_item)
            .service(create_item)
    })
    .bind(("0.0.0.0", 5000))?
    .run()
    .await
}
