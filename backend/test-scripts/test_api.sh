echo "=== Testing Health Check ==="
curl http://localhost:5000/health
echo -e "\n\n"

echo "=== Testing Normal Message ==="
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I feel overwhelmed with assignments"}'
echo -e "\n\n"

echo "=== Testing Crisis Detection ==="
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I feel like ending my life"}'
echo -e "\n\n"

echo "=== Testing Empty Message ==="
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'
echo -e "\n\n"
