from registry import *



def chat(client, model, history, temperature, top_p, max_tokens, tools):
  result = client.chat.completions.create(
        model=model,
        messages=history,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        tools=tools,
        tool_choice="auto",
    )

  tool_calls = result.choices[0].message.tool_calls
  if tool_calls is not None:
      fun_name = tool_calls[0].function.name
      fun_args = tool_calls[0].function.arguments
      bot_response = eval(f"{fun_name}(**{fun_args})")
  else:
      bot_response = result.choices[0].message.content
      
  return bot_response