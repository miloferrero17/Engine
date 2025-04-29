from supabase import create_client
import os

# 🔐 Tus credenciales Supabase (completas y explícitas)
SUPABASE_URL = "https://wquudugppahrfcuiikdy.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndxdXVkdWdwcGFocmZjdWlpa2R5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM0MzM5MDIsImV4cCI6MjA1OTAwOTkwMn0._N18O6gXcVCto8gkKGzrZKnz2OUGGqomAuEJ99zNXBc"

# Inicializamos el cliente
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# Hacemos una consulta de prueba (a una tabla "users" que vos tengas creada)
try:
    response = supabase.table("users").select("*").limit(3).execute()
    print("✅ Datos recibidos de Supabase:")
    print(response.data)
except Exception as e:
    print("❌ Error al consultar Supabase:", e)

