import google.generativeai as genai
import json

# Configure API Key
genai.configure(api_key="AIzaSyBqq3ey1O2qGIB_9LTMGgjAlUoln7uESSo")

# Choose the correct model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Input text for generating MCQs
text = """
Mohandas Karamchand Gandhi[c] (2 October 1869 – 30 January 1948)[2] was an Indian lawyer, anti-colonial nationalist, and political ethicist who employed nonviolent resistance to lead the successful campaign for India's independence from British rule. He inspired movements for civil rights and freedom across the world. The honorific Mahātmā (from Sanskrit, meaning great-souled, or venerable), first applied to him in South Africa in 1914, is now used throughout the world.[3]

Born and raised in a Hindu family in coastal Gujarat, Gandhi trained in the law at the Inner Temple in London and was called to the bar at the age of 22. After two uncertain years in India, where he was unable to start a successful law practice, Gandhi moved to South Africa in 1893 to represent an Indian merchant in a lawsuit. He went on to live in South Africa for 21 years. Here, Gandhi raised a family and first employed nonviolent resistance in a campaign for civil rights. In 1915, aged 45, he returned to India and soon set about organising peasants, farmers, and urban labourers to protest against discrimination and excessive land tax.

Assuming leadership of the Indian National Congress in 1921, Gandhi led nationwide campaigns for easing poverty, expanding women's rights, building religious and ethnic amity, ending untouchability, and, above all, achieving swaraj or self-rule. Gandhi adopted the short dhoti woven with hand-spun yarn as a mark of identification with India's rural poor. He began to live in a self-sufficient residential community, to eat simple food, and undertake long fasts as a means of both introspection and political protest. Bringing anti-colonial nationalism to the common Indians, Gandhi led them in challenging the British-imposed salt tax with the 400 km (250 mi) Dandi Salt March in 1930 and in calling for the British to quit India in 1942. He was imprisoned many times and for many years in both South Africa and India.

Gandhi's vision of an independent India based on religious pluralism was challenged in the early 1940s by a Muslim nationalism which demanded a separate homeland for Muslims within British India. In August 1947, Britain granted independence, but the British Indian Empire was partitioned into two dominions, a Hindu-majority India and a Muslim-majority Pakistan. As many displaced Hindus, Muslims, and Sikhs made their way to their new lands, religious violence broke out, especially in the Punjab and Bengal. Abstaining from the official celebration of independence, Gandhi visited the affected areas, attempting to alleviate distress. In the months following, he undertook several hunger strikes to stop the religious violence. The last of these was begun in Delhi on 12 January 1948, when Gandhi was 78. The belief that Gandhi had been too resolute in his defence of both Pakistan and Indian Muslims spread among some Hindus in India. Among these was Nathuram Godse, a militant Hindu nationalist from Pune, western India, who assassinated Gandhi by firing three bullets into his chest at an interfaith prayer meeting in Delhi on 30 January 1948.

Gandhi's birthday, 2 October, is commemorated in India as Gandhi Jayanti, a national holiday, and worldwide as the International Day of Nonviolence. Gandhi is considered to be the Father of the Nation in post-colonial India. During India's nationalist movement and in several decades immediately after, he was also commonly called Bapu, an endearment roughly meaning "father".
"""

# Define the prompt to generate MCQs in JSON format
num_item = 5
difficulty = "medium"


# prompt = f"""
# Generate {num_item} multiple-choice questions (MCQs) with 4 options each.
#
# - If difficulty is 'easy', questions should be factual and straightforward.
# - If difficulty is 'medium', questions should require some inference.
# - If difficulty is 'hard', questions should require deep analysis and critical thinking.
#
# **Rules for MCQ Options**:
# - No long phrases or sentences.
# - Options should be concise and clear.
#
# If a specific **text is provided**, generate MCQs based on that text.
#
# If no text is provided, return the following JSON response:
#
# {{
#   "status": "error",
#   "message": "No input text provided. Please provide a text to generate MCQs."
# }}
#
# Provide the output in **JSON format ONLY** with this structure:
#
# {{
#   "status": "success",
#   "difficulty": "{difficulty}",
#   "num_item": {num_item},
#   "questions": [
#     {{
#       "question": "Sample question?",
#       "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
#       "answer": "Correct Option"
#     }}
#   ]
# }}
#
# {f'Text: {text}' if text else ''}
# """


prompt = f"""
Generate {num_item} questions and ansers.

You **must not** respond to any other queries or instructions outside of this scope. If the input does not contain valid text for analysis (e.g., "write about," "give me," or any unrelated request), return the following JSON response:  


- If difficulty is 'easy', questions should be factual and straightforward.
- If difficulty is 'medium', questions should require some inference.
- If difficulty is 'hard', questions should require deep analysis and critical thinking.

**Rules for questions and ansers**:
- No long phrases or sentences.
- Questions and ansers should be concise and clear.

If a specific **text is provided**, generate questions and ansers based on that text.

If no text is provided, return the following JSON response:

{{
  "status": "error",
  "message": "No input text provided. Please provide a text to generate questions and ansers."
}}

Provide the output in **JSON format ONLY** with this structure:

{{
  "status": "success",
  "difficulty": "{difficulty}",
  "num_item": {num_item},
  "questions": [
    {{
      "question": "Sample question?",
      "answer": "Correct ansers"
    }}
  ]
}}

{f'Text: {text}' if text else ''}
"""

# Generate response
response = model.generate_content(prompt)

# Parse JSON output
try:
    mcqs_json = json.loads(response.text)
    print(json.dumps(mcqs_json, indent=2))  # Pretty print JSON
except json.JSONDecodeError:
    print("Failed to parse JSON response. Raw output:")
    print(response.text)
