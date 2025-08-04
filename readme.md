markdown# Semantic Search Project

A FastAPI-based semantic search engine for permit documents using OpenAI embeddings and ChromaDB vector storage. This project enables intelligent search through permit data using natural language queries with advanced filtering capabilities.

## 🌟 Features

- **Semantic Search**: Natural language search using OpenAI's text-embedding-3-small model
- **Vector Storage**: Efficient storage and retrieval using ChromaDB with cosine similarity
- **Advanced Filtering**: Filter search results by metadata fields
- **FastAPI Backend**: High-performance async API with automatic documentation
- **Query Logging**: Comprehensive logging of all search queries for analytics
- **Health Monitoring**: Built-in health check endpoint
- **Flexible Results**: Configurable number of results with similarity scores

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- 2GB+ free disk space for ChromaDB storage

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/muneebfrfr/sementic_search_project.git
   cd sementic_search_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "OPENAI_KEY=your_openai_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the API**
   - API: `http://localhost:8000`
   - Interactive Docs: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## 📁 Project Structure

```
sementic_search_project/
├── main.py                           # Main FastAPI application
├── requirements.txt                  # Python dependencies
├── .env                             # Environment variables (create this)
├── query_logs.log                   # Search query logs (auto-generated)
├── final_permits_chroma_storage/    # ChromaDB persistent storage (auto-generated)
└── README.md                        # This file
```

## 🔧 API Endpoints

### Search Permits

**POST** `/search`

Search through permit documents using natural language queries with optional filtering.

#### Request Body

```json
{
  "query": "building permits for commercial construction",
  "filters": {
    "permit_type": "commercial",
    "status": "approved"
  },
  "top_k": 5
}
```

#### Request Schema

| Field    | Type                    | Required | Default | Description                           |
|----------|-------------------------|----------|---------|---------------------------------------|
| query    | string                  | Yes      | -       | Natural language search query         |
| filters  | object                  | No       | null    | Key-value pairs for metadata filtering|
| top_k    | integer                 | No       | 5       | Number of results to return           |

#### Response

```json
{
  "results": [
    {
      "document": "Commercial building permit for 123 Main St...",
      "metadata": {
        "permit_type": "commercial",
        "status": "approved",
        "date_issued": "2024-08-01",
        "location": "123 Main St"
      },
      "similarity_score": 0.8945
    }
  ]
}
```

#### Example Usage

```bash
# Basic search
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "residential building permits"
     }'

# Search with filters
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "construction permits",
       "filters": {
         "permit_type": "residential",
         "status": "pending"
       },
       "top_k": 10
     }'
```

### Health Check

**GET** `/healthz`

Check if the API is running properly.

#### Response

```json
{
  "ok": true
}
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_KEY=your_openai_api_key_here

# Optional: Server Configuration
HOST=0.0.0.0
PORT=8000
```

### ChromaDB Configuration

The application uses ChromaDB with the following settings:
- **Storage Path**: `./final_permits_chroma_storage`
- **Collection Name**: `permits_vector_data`
- **Similarity Metric**: Cosine similarity
- **Embedding Model**: OpenAI text-embedding-3-small

## 🧪 Testing the API

### Using Python

```python
import requests

# Basic search
response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "building permits for commercial properties",
        "top_k": 3
    }
)
print(response.json())

# Search with filters
response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "construction permits",
        "filters": {
            "permit_type": "residential",
            "status": "approved"
        },
        "top_k": 5
    }
)
print(response.json())
```

### Using JavaScript/Node.js

```javascript
const fetch = require('node-fetch');

async function searchPermits() {
  const response = await fetch('http://localhost:8000/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: 'residential building permits',
      filters: {
        status: 'approved'
      },
      top_k: 5
    })
  });
  
  const data = await response.json();
  console.log(data);
}

searchPermits();
```

## 📊 Features Deep Dive

### Semantic Search

The application uses OpenAI's `text-embedding-3-small` model to convert text into high-dimensional vectors. This enables:
- **Contextual Understanding**: Finds documents based on meaning, not just keywords
- **Synonym Recognition**: Matches related terms automatically
- **Natural Language Queries**: Search using conversational language

### Advanced Filtering

Supports complex filtering with the `$and` operator:
```json
{
  "query": "building permits",
  "filters": {
    "permit_type": "commercial",
    "status": "approved",
    "city": "New York"
  }
}
```

### Query Logging

All searches are logged to `query_logs.log` with:
- Timestamp
- Search query
- Applied filters
- Results metadata

Example log entry:
```
2024-08-04 10:30:15,123 - INFO - Search Query Log: {
  "query": "building permits", 
  "filters": {"status": "approved"}, 
  "top_results": {...}
}
```

## 📈 Performance

- **Embedding Generation**: ~100-200ms per query
- **Vector Search**: <50ms for typical datasets
- **API Response Time**: ~200-300ms end-to-end
- **Concurrent Requests**: Supports multiple simultaneous searches
- **Memory Usage**: ~500MB-1GB depending on dataset size

## 🛠️ Technology Stack

- **Web Framework**: FastAPI 0.100+
- **Vector Database**: ChromaDB with persistent storage
- **Embeddings**: OpenAI text-embedding-3-small
- **HTTP Client**: OpenAI Python SDK
- **Server**: Uvicorn ASGI server
- **Data Validation**: Pydantic models
- **Environment**: python-dotenv

## 🚀 Deployment

### Local Development

```bash
python main.py
```

### Production Deployment

#### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t semantic-search .
docker run -p 8000:8000 --env-file .env semantic-search
```

#### Using Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  semantic-search:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./final_permits_chroma_storage:/app/final_permits_chroma_storage
      - ./query_logs.log:/app/query_logs.log
```

Run: `docker-compose up -d`

## 📦 Dependencies

```txt
fastapi>=0.100.0
uvicorn[standard]>=0.20.0
chromadb>=0.4.0
openai>=1.0.0
python-dotenv>=1.0.0
pydantic>=2.0.0
```

## 🔍 How It Works

1. **Query Processing**: User submits natural language query via POST request
2. **Embedding Generation**: Query is converted to vector using OpenAI's embedding API
3. **Vector Search**: ChromaDB performs cosine similarity search against stored document embeddings
4. **Filtering**: Optional metadata filters are applied using ChromaDB's `where` clause
5. **Results Ranking**: Results are ranked by similarity score and returned
6. **Logging**: Query details are logged for analytics and monitoring

## 🐛 Troubleshooting

### Common Issues

**OpenAI API Key Error**
```
Error: OpenAI API key not found
```
Solution: Ensure your `.env` file contains `OPENAI_KEY=your_api_key`

**ChromaDB Connection Error**
```
Error: Cannot connect to ChromaDB
```
Solution: Ensure the `final_permits_chroma_storage` directory has proper permissions

**Empty Results**
```
{"results": []}
```
Solution: Check if documents are properly indexed in ChromaDB collection

### Debug Mode

Run with debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/muneebfrfr/sementic_search_project/issues)
- **Developer**: [Muneeb](https://github.com/muneebfrfr)

## 🔮 Future Enhancements

- [ ] Document upload and indexing API
- [ ] Batch search capabilities
- [ ] Authentication and authorization
- [ ] Rate limiting
- [ ] Caching layer for frequent queries
- [ ] Support for multiple embedding models
- [ ] Analytics dashboard
- [ ] Export search results

---

**Made with ❤️ by [Muneeb](https://github.com/muneebfrfr)**