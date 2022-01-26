import openai, os

openai.api_key = os.environ.get('OPENAI_API_KEY')
ft_model = "curie:ft-personal-2022-01-25-20-15-32"
prompt = input("Prompt: ")
endloop = False
while not endloop:
    response = openai.Completion.create(model=ft_model, prompt=prompt + " -> ", max_tokens=100, temperature=0.7, stop="END")
    final = "\n".join(response.choices[0].text.lstrip(" ").split("\n")[:-1]).replace(".", "")
    
    if final.count("\n") > 2:
        endloop = True
        print(final)