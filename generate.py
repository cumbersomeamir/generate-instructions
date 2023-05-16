#pip3 install openai pandas openpyxl

import openai
import pandas as pd
import random
import re
import openpyxl

df = pd.read_excel("all_instructions 228.xlsx")
print(df)
print(len(df))

#Global Initialisations
all_instructions = df["Instructions"]
number_of_samples = 8
instructions_per_batch = 100
total_iterations = 3
#Converting Pandas dataframe into a list
all_instructions_list = list(all_instructions)

#Generate instruction function
def generate_instruction(batch, instructions_per_batch):
  #Setting the openai api key
  context = f"I have the following 8 samples of instructions. Please generate {instructions_per_batch} more instructions which are similar to these. Please keep the instructions as general as possible"
  openai.api_key = "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"

  #Prepending the prompt with the context
  content = context + str(batch)
  response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = [{"role": "user", "content": content}])
  new_instruction = response['choices'][0]['message']['content']
  return new_instruction

#Random Sampling Function
def get_random_instructions(all_instructions, number_of_samples):
  if len(all_instructions) < number_of_samples:
        return "The number of samples required is more than the number of instructions available."
  else:
        return random.sample(all_instructions, number_of_samples)




for iteration in range(total_iterations):
    print("The iteration number is ", iteration)

    # Random Sampling the Batch
    batch = get_random_instructions(all_instructions_list, number_of_samples)

    # Generating 100 instructions per Batch
    generated_instructions = generate_instruction(batch, instructions_per_batch)

    # Converting str to a new_list
    # Use regular expressions to match and split on the digit sequences
    split_string = re.split(r'\d+\.', generated_instructions)

    # Remove the first empty string if present (it will be present if your string starts with a number)
    if not split_string[0]:
        split_string = split_string[1:]

    # Create the new_list of instructions that we just generated
    new_list = [s.strip() for s in split_string]

    # Adding newly generated instructions to all_instructions

    # Getting the length before merging
    print("The original length is", len(all_instructions_list))

    # Merging the new_list to all_instructions_list
    all_instructions_list = all_instructions_list + new_list
    print("The length of the updated list is", len(all_instructions_list))

    # Save to Excel every 50 iterations
    if iteration % 2 == 0:
        df = pd.DataFrame(all_instructions_list, columns=["Instructions"])
        df.to_excel(f'all_instructions_{iteration}.xlsx', index=False)

