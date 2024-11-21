# Investors Diary

An intelligent LLM Agent-based personal diary that manages stock purchases and sales using natural language interaction. The application leverages advanced language models to understand user intent, process requests, and maintain detailed records of stock transactions along with reasoning behind investment decisions.

## 🌟 Features

### Natural Language Interaction
- Communicate with the assistant using everyday language
- Intelligent parsing of transaction details
- Context-aware responses and clarifications
- Multi-turn conversations for complex queries

### Transaction Management
- Record stock purchases and sales with detailed metadata
- Track transaction dates, quantities, and prices
- Store reasoning behind investment decisions
- Automatic calculation of total transaction amounts
- Support for multiple transaction types (buy/sell)

### Investment Analysis
- Review historical transaction patterns
- Generate insights from past investment decisions
- Search and filter transactions by various parameters
- Track performance across different sectors
- Analyze investment distribution

### Market Research
- Integrated stock research capabilities
- Real-time market data integration
- Company information lookup
- Sector-specific analysis
- Automated research summaries

### Data Management
- Secure SQLite database storage
- Vector-based search for transaction notes
- Efficient data retrieval and querying
- Data backup and export capabilities

## 🚀 Technology Stack

- **Backend Framework**: FastAPI
- **Frontend**: Streamlit
- **Database**: SQLite with FAISS vector store
- **AI/ML**: 
  - LangChain Framework
  - OpenAI GPT Models
- **Development**: 
  - Python 3.10+
  - Poetry for dependency management

## 📋 Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Poetry package manager
- Git (for version control)

## 💻 Installation

1. Clone the repository:
```bash
git clone https://github.com/kirushikesh/investors-diary.git
cd investors-diary
```
2. Install dependencies using Poetry:
```bash
poetry install
```
3. Set up environment variables:
```bash
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```
## 🎯 Usage
1. Start the FastAPI server:
```bash
poetry run python src/app/server.py
```
2. Launch the Streamlit interface:
```bash
poetry run python src/app/client.py
```

(OR)

1. Run the Agent in CLI
```bash
poetry run python src/core/graph_builder.py
```

Example interactions:
- "I Bought 100 shares of AAPL at $150 each today"
- "Show me all my Tesla transactions from last month"
- "What was my reasoning for selling Microsoft shares?"
- "Research the current market position of Amazon"
- ....


## 🏗️ Project Structure
```
investors-diary/
├── src/
│   ├── agents/              # LLM agent implementations
│   │   ├── analysis_agent.py
│   │   ├── research_agent.py
│   │   └── transaction_agent.py
|   |   ...
│   ├── database/            # Database models and operations
│   ├── tools/               # Custom tools for agents
│   ├── prompts/             # Prompt templates
│   └── utils/               # Helper utilities
├── tests/                   # Test suite
├── data/                    # Data storage
└── notebooks/              # Development notebooks
```

## 🏗️ Technical Architecture

### LangGraph Implementation
The project leverages LangGraph, a powerful framework for building stateful, multi-agent workflows, to create a sophisticated investment management system. LangGraph facilitates:

- State management across multiple agent interactions
- Directed graph-based workflow orchestration
- Conditional routing between different agents
- Structured message passing between components

### Supervisor Design Pattern
The main application follows the Supervisor design pattern, implemented using LangGraph's StateGraph:

```python
builder = StateGraph(MainState)
```

### Core Components:
1. Primary Assistant (Supervisor)
- Acts as the central coordinator
- Routes user requests to specialized agents
- Manages workflow transitions
- Handles task delegation and completion

2. Specialized Agents
- Transaction Agent: Handles stock purchases and sales
- Analysis Agent: Processes transaction analysis requests
- RAG Agent: Manages retrieval of user stock notes
- Research Agent: Conducts stock market research

Workflow Management:
```python
builder.add_conditional_edges(
    "primary_assistant",
    route_primary_assistant,
    [
        "enter_add_transactions",
        "enter_retrieve_transactions",
        "enter_find_notes",
        "enter_research_stock_news",
        "primary_assistant_tools",
        END,
    ],
)
```

### Stock Researcher's Reflexion Pattern
The Stock Research component uniquely implements the Reflexion design pattern, enabling self-improvement through iterative refinement:

```python
sub_builder = StateGraph(SUBState)
sub_builder.add_node("draft", ResearchAgent)
sub_builder.add_node("execute_tools", create_tool_node_with_fallback(research_agents_tools))
sub_builder.add_node("revise", RevisorAgent)
```

Key Features:
1. Initial Draft
- Creates initial research response
- Utilizes available tools and context
2. Self-Reflection
- Analyzes response quality
- Identifies missing information
- Evaluates response completeness
3. Iterative Improvement
- Conducts additional research based on reflection
- Refines answer through multiple iterations
- Maximum iterations controlled: MAX_ITERATIONS = 2

### State Management
Uses LangGraph's state management to maintain context across interactions
Implements checkpointing using MemorySaver:
```python
memory = MemorySaver()
main_graph = builder.compile(
    checkpointer=memory,
)
```

### Tool Integration
- Custom tools for each agent type
- Fallback mechanisms for error handling
- Structured tool responses using Pydantic models

### Key Benefits of This Architecture
1. Modularity: Each agent handles specific responsibilities
2. Scalability: Easy to add new agents and functionalities
3. Maintainability: Clear separation of concerns
4. Reliability: Built-in error handling and fallback mechanisms
5. Flexibility: Easy to modify workflow routing and agent behavior
This architecture enables the system to handle complex investment-related queries while maintaining context and providing accurate, well-researched responses through a combination of specialized agents and sophisticated control flow management.

## Future Directions
### Enhanced Analytics
1. Portfolio performance visualization
2. Custom reporting capabilities
3. Real-time price alerts and notifications
4. Multi-user support with authentication
5. Integration with financial news APIs
6. Adding Long-Term memory for each user for customized interactions

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 References
- LangGraph Supervisor design pattern: https://langchain-ai.github.io/langgraph/tutorials/customer-support/customer-support/
- LangGraph Reflexion pattern: https://langchain-ai.github.io/langgraph/tutorials/reflexion/reflexion/
- LangServe Connectivity: https://python.langchain.com/docs/langserve/
