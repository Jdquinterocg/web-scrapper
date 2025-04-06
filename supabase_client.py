import os
from datetime import datetime
from supabase import create_client

# Obtener las credenciales de Supabase desde variables de entorno
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Crear el cliente de Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_exchange_rates(usd_rate, eur_rate, bank_name="BBVA"):
    try:
        # Calcular los valores ajustados
        adjusted_usd = round(float(usd_rate) + 0.50, 4)
        adjusted_eur = round(float(eur_rate) + 0.50, 4)

        # Preparar los datos para insertar
        data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "usd_rate_original": float(usd_rate),
            "eur_rate_original": float(eur_rate),
            "usd_rate_adjusted": adjusted_usd,
            "eur_rate_adjusted": adjusted_eur,
            "bank_name": bank_name,
            "created_at": datetime.now().isoformat(),
        }

        # Insertar los datos en la tabla 'exchange_rates'
        supabase.table("exchange_rates").insert(data).execute()

        print(f"Data saved successfully to Supabase: {data}")
        return True
    except Exception as e:
        print(f"Error saving to Supabase: {str(e)}")
        return False
