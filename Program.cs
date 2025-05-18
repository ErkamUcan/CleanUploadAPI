var builder = WebApplication.CreateBuilder(args);

// Servisleri ekle
builder.Services.AddControllers();

// 🔐 CORS: React 3000 portundan gelen istekleri kabul et
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowReactApp", policy =>
    {
        policy.WithOrigins("http://localhost:3000")
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

var app = builder.Build();

// 🔧 HTTPS yönlendirmesi
// app.UseHttpsRedirection();

// ✅ CORS middleware — authorization'dan önce olmalı
app.UseCors("AllowReactApp");

app.UseAuthorization();

app.MapControllers();

app.Run();
