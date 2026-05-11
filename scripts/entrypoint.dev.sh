set -e

echo "🔧 Starting development entrypoint..."

python scripts/wait_for_dependencies.py

echo "📦 Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "🚀 Starting Django dev server..."
python manage.py runserver 0.0.0.0:8000