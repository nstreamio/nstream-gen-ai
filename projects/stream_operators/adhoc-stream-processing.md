# Real-Time, Ad-hoc Stream Processing with OpenAI and SwimOS: Automating Dynamic Stream Operators

## Introduction

In modern applications, the need for real-time data processing is ever-growing, particularly in domains like finance, 
IoT, and large-scale monitoring. Integrating **Generative AI** with **real-time stream processing** offers an innovative 
approach to managing complex workflows, enabling dynamic generation, validation, and execution of stream operators based 
on natural language inputs.

In this blog post, we will walk through an exciting system that leverages **OpenAI's Generative AI** capabilities for 
the automatic creation of stream processing operators, powered by **SwimOS**, a platform for building real-time, 
streaming data applications. This integration enables dynamic, on-the-fly operations that simplify managing complex, 
evolving streams of data. We’ll dive into the architecture, the underlying Python code, and the complete workflow.

### Setting the Stage

Before we get into the technical depth, let's first understand the broader architecture and how OpenAI and SwimOS work 
together. Here's the high-level system flow:

- **Natural Language Queries**: The system accepts natural language commands from the user, simplifying the interaction. For instance, a user might request, "accumulate the average stock prices for XYZ."
- **OpenAI's NLU & Generation**: OpenAI interprets the query, identifies the appropriate stream operation, and generates the corresponding Python code.
- **SwimOS Stream Processing**: SwimOS then integrates the generated operators, validates them, and executes them in real-time on live data streams.

#### High-Level Architecture

[Insert the image with **Natural Language** → **OpenAI + SwimOS** → **Real-time Continuous Response**]

This diagram represents the overall workflow, showing how natural language queries translate into real-time stream 
operations. The process involves three key stages:

1. **Natural Language Query**: Users issue commands.
2. **OpenAI + SwimOS Workflow**: The core of the system where the query is processed.
3. **Real-time Continuous Response**: The results of the stream processing are sent back to the user.

### Core Functionality – Fabrication Stage

At the heart of the system lies the **OpenAI + SwimOS Workflow Stage**, where OpenAI generates code that SwimOS integrates into its 
streaming architecture. In the previous diagram, **Workflow** was highlighted to emphasize 
its importance as the core functionality.

#### OpenAI + SwimOS Workflow Breakdown

[Insert Diagram 2 with **Identification (OpenAI)** → **Fabrication (OpenAI + SwimOS)** → **Validation (SwimOS)**]

Here’s a breakdown of each stage:

1. **Identification**: This is handled by OpenAI’s NLU (Natural Language Understanding), which interprets user queries and identifies the required stream operator.
2. **Fabrication**: OpenAI generates the Python code for the required operator (e.g., to map, filter, or accumulate data). SwimOS contextualizes this code within the streaming framework. This is the **core stage** where OpenAI and SwimOS collaborate.
3. **Validation**: SwimOS checks whether the generated code is valid for the current streaming architecture. If validation fails, the system flows back to **Fabrication** for code adjustment.

When validation succeeds, the stream operator is integrated, and the system processes real-time data accordingly. If 
validation fails, it loops back to Fabrication, where the operator is regenerated or modified.

### Key Python Code for Operator Generation

Let’s now dive into the technical implementation. Below is a snippet of the code responsible for generating one form of 
stream operator using OpenAI's generative capabilities and SwimOS’s ability to validate domain and stream processing 
context.

```python
@app.command()
def accumulate_generate(symbol: str, streaming_operator: str, operation_config: str = typer.Option("{}")):
    global acc
    acc = {}

    # Parse the operation_config JSON string
    current_operation_config = json.loads(operation_config)
    parameters = json.dumps(current_operation_config)

    prompt = f"""
    Return a JSON result, and only a JSON result. The JSON must have a single top-level key: `result`.
    The JSON should contain a Python function with the signature:
    `def func(acc: dict, new_value: float, params: dict):`
    The function should compute {streaming_operator} on `new_value` and update `acc` based on each new value.
    """
    
    function_code_str = generate_llm_code(prompt, expect_json=True)

    # Evaluate the function code
    local_vars = {}
    exec(function_code_str, {}, local_vars)
    func = local_vars["func"]

    def accumulate_generate_callback(new_value: dict, _old_value: dict):
        global acc
        acc, summary = func(acc, new_value['price'], current_operation_config)
        print(f"{symbol} -- summary: {summary}; acc: {acc}")

    node_uri = f"/stock/{symbol}"
    value_downlink = setup_value_downlink(node_uri, accumulate_generate_callback)
```

#### Breakdown

- **accumulate_generate**:
  - This function handles generating the code to accumulate stock prices over time, using OpenAI to generate Python code dynamically.
- **LLM Prompting**:
  - The prompt instructs OpenAI to generate a function with the signature `def func(acc: dict, new_value: float, params: dict)`. The operator (e.g., average, min, max) is incorporated into the function, and the code is executed in real-time to process incoming stream data.
- **SwimOS Integration**:
  - After generating the operator, SwimOS validates and integrates the operator within its real-time streaming context, ensuring it fits the architecture.

This dynamic generation process allows users to customize stream operators on the fly, creating immense flexibility in 
real-time data processing scenarios.

### Error Handling and the Conditional Loop

A key part of the system is the **Validation** stage. If the operator generated by OpenAI fails during validation in 
SwimOS, the system loops back to **Fabrication** to adjust the operator. This loop ensures that the system can handle 
unexpected conditions, regenerate the operator if necessary, and continue functioning without disruption.

#### Code Handling Retries:

```python
def generate_llm_code_for_execute(prompt: str, max_retries: int = 5, retry_delay: int = 1):
    retries = 0
    while retries < max_retries:
        try:
            response = llm_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4",
                max_tokens=1000
            )
            response_content = response.choices[0].message.content.strip()
            json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(0))
                return result
        except Exception as e:
            retries += 1
            time.sleep(retry_delay)
```

This retry mechanism ensures that the system robustly handles edge cases, such as invalid code generation or network 
issues, by making multiple attempts before failing.

### The Full Workflow in Action

Let’s walk through an example to see this system in action:

1. The user issues a query: “accumulate the average stock prices for symbol XYZ.”
2. OpenAI identifies the task and generates the Python function to accumulate averages.
3. SwimOS integrates the operator, validates it, and begins processing real-time stock prices, calculating averages on the fly.
4. If validation fails, SwimOS loops back to OpenAI, regenerates the operator, and continues processing.

This process, powered by AI-driven operator generation and real-time validation, unlocks powerful new ways of managing 
and interacting with streaming data.

### Conclusion

The integration of **OpenAI** with **SwimOS** brings power and flexibility to real-time stream processing. By 
automating the generation of custom stream operators using natural language inputs, this approach simplifies complex 
workflows while enabling powerful dynamic responses. Whether it’s filtering, mapping, or accumulating data, this 
architecture offers a highly scalable solution for real-time data challenges.

Hopefully this post provided you with insight into how real-time stream processing can be enhanced with Generative AI. 
Stay tuned for more developments and deep dives into intersections of generative AI and real-time stream processing!

**Next steps**: 
- **Download the Full Source Code**: [Link to GitHub repo]
- **Try it Yourself**: Set up your own real-time stream processing with OpenAI and SwimOS using the provided code.