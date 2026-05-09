FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY ["dotnet-api.csproj", "./"]
RUN dotnet restore "dotnet-api.csproj"
COPY . .
RUN dotnet publish "dotnet-api.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish ./
EXPOSE 5000
ENTRYPOINT ["dotnet", "dotnet-api.dll"]
