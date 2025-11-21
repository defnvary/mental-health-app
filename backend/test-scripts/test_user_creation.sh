curl -X POST http://localhost:5000/create-user \
  -H "Content-Type: application/json" \
  -d '{"email":"doctor1@example.com","password":"secure123"}'