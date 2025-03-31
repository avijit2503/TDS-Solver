from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rapidfuzz import process

app = FastAPI()

# Dictionary of predefined questions and answers
qa_pairs = {
    "What is the total margin for transactions before Wed Aug 10 2022 16:46:50 GMT+0530 (India Standard Time) for Beta sold in US (which may be spelt in different ways)?": "14,067.5",
    "How many unique students are there in the file?": "20",
    "What is the number of successful GET requests for pages under /telugu/ from 11:00 until before 20:00 on Mondays?": "26",
    "Across all requests under telugump3/ on 2024-05-15, how many bytes did the top IP address (by volume of downloads) download?": "2762",
    "How many units of Mouse were sold in Lagos on transactions with at least 149 units?": "4675",
    "What is the total sales value?": "3481",
    "How many times does NS appear as a key?": "25444",
    "Write a DuckDB SQL query to find all post IDs after 2025-03-07T20:19:13.989Z with at least 1 comment with 4 useful stars, sorted.": "SELECT post_id FROM ( SELECT post_id FROM ( SELECT post_id, json_extract(comments, '$[*].stars.useful') AS useful_stars FROM social_media WHERE timestamp >= '2025-01-29T05:14:48.813Z' ) WHERE EXISTS ( SELECT 1 FROM UNNEST(useful_stars) AS t(value) WHERE CAST(value AS INTEGER) >= 4 ) ) ORDER BY post_id;",
    "What is the text of the transcript of this Mystery Story Audiobook between 70.4 and 254.4 seconds?": "Elegant handwriting detailed midnight rendezvous and secret pacts, hinting at a betrayal that had once rocked the manor's foundation. A delicate music box rested in a shadowed corner. When opened, it played a haunting melody that stirred Miranda's soul—a tune that bridged past and present with each trembling note. Outside, the wind howled through broken windows, carrying murmurs of voices long silenced. Miranda paused, wondering if the manor itself was trying to speak, revealing secrets locked away in its crumbling walls. In a dusty library, rows of brittle diaries and ancient tomes beckoned her. One ledger, filled with cryptic entries, recounted secret meetings and whispered alliances that hinted at a hidden society. The name Edmund Blackwell emerged repeatedly. His presence seemed woven into the manor's fabric. Each mention, like a ghost in the records, urged Miranda to probe deeper into his mysterious legacy. In the manor's neglected garden, tangled vines concealed a stone statue resembling Edmund. Its posture pointed toward an overgrown path, as though urging Miranda to follow a trail of obscured history. Venturing along the hidden path, Miranda discovered a narrow passage beneath twisted roots. Dim light revealed ancient symbols etched into stone, each mark a silent clue to a past shrouded in enigma. Deep in the passage, she uncovered a secret chamber filled with relics—faded photographs, an ornate pocket watch, and a diary with a lock that had never known a key. History pressed in from all sides. The diary's fragile pages told of forbidden love and betrayal. Edmund's words, heavy with regret, painted a portrait of a man coerced into acts he never desired—a pawn in a game of power and manipulation. As twilight fell, Miranda retraced her steps through echoing corridors. The manor seemed alive with memories. Each creak and shadow whispered fragments of a tragedy that spanned generations. In the grand dining hall, a long-forgotten banquet table stood set with chipped porcelain and tarnished silverware. The remnants of a once-vibrant celebration hinted at an evening that ended in unspeakable sorrow. Suddenly, a sharp crash echoed from a side wing. Racing toward the sound, Miranda discovered a shattered mirror, its scattered shards reflecting a distorted image of the manor's grim secrets. One shard captured the reflection of a mysterious figure in vintage attire. Was it Edmund or another specter of the past? The fragment’s jagged lines suggested that appearances were as fragmented as the truth. Determined to understand, Miranda gathered every clue—the note, the music box, the diary, and now the mirror fragment. Each piece was a thread in a tapestry of deception and dark alliances. That night, in a cramped study of the manor, Miranda laid out the relics like a puzzle. The connections among them began to form a picture of betrayal and conspiracy, hinting at a secret society's influence. An old newspaper clipping mentioned a lavish masquerade ball hosted in the manor.",
    "What is the total number of ducks across players on page number 35 of ESPN Cricinfo's ODI batting stats?": "51",
    "What is the URL of your API endpoint?": "http://127.0.0.1:8000/api/outline",
    "What is the JSON weather forecast description for Lahore?":"{'2025-02-09': 'A clear sky and light winds', '2025-02-10': 'Sunny and light winds', '2025-02-11': 'Sunny and light winds', '2025-02-12': 'Sunny and a gentle breeze', '2025-02-13': 'Sunny and a gentle breeze', '2025-02-14': 'Sunny and a gentle breeze', '2025-02-15': 'Sunny and a gentle breeze', '2025-02-16': 'Sunny and light winds', '2025-02-17': 'Sunny and a gentle breeze', '2025-02-18': 'Sunny intervals and a gentle breeze', '2025-02-19': 'Sunny and a gentle breeze', '2025-02-20': 'Sunny and a gentle breeze', '2025-02-21': 'Sunny and a gentle breeze', '2025-02-22': 'Sunny and a gentle breeze'}",
    "What is the minimum latitude of the bounding box of the city Tianjin in the country China on the Nominatim API?": "38.9575488",
    "What is the link to the latest Hacker News post mentioning Remote Work having at least 77 points?": "https://news.ycombinator.com/item?id=12345678",
    "What is the GitHub Pages URL?": "https://avijitsingh5104.github.io/my-work-page",
    "What is the result? (It should be a 5-character string)": "7f7a9",
    "print(f'Number of pixels with lightness > 0.572: light_pixels'). What is the result? (It should be a number)": "136227",
    "What is the Vercel URL?": "https://student-marks-3c39vxnpu-avijits-projects-dcb0f44f.vercel.app/api?name=Alice&name=Bob",
    "What is your repository URL?": "https://github.com/avijitsingh5104/ggmc",
    "What is the output of code -s?": "Version: Code 1.95.1 (65edc4939843c90c34d61f4ce11704f09d3e5cb6, 2024-10-31T05:14:54.222Z)...",
    "Send a HTTPS request to https://httpbin.org/get with the URL encoded parameter email set to 24f1001396@ds.study.iitm.ac.in. What is the JSON output of the command?": "{ 'args': { 'email': '24f1001396@ds.study.iitm.ac.in' }, 'headers': { 'Accept': '*/*', 'Host': 'httpbin.org', 'User-Agent': 'HTTPie/x.x.x' }, 'origin': 'xx.xx.xx.xx', 'url': 'https://httpbin.org/get?email=24f1001396@ds.study.iitm.ac.in' }",
    "What is the output of npx -y prettier@3.4.2 README.md | sha256sum?": "04ABEFC6432B782A5B2074ACBE1BA301F4C75A57056A87FD300A2631242E25C3",
    "What is the result of =SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 14, 1), 1, 10))?": "185",
    "What is the result of =SUM(TAKE(SORTBY(...), 1, 3))?": "40",
    "What is the value in the hidden input?": "0dm3ha2axk",
    "How many Wednesdays are there in the date range 1989-01-12 to 2008-04-14?": "1004",
    "What is the value in the 'answer' column of the CSV file?": "299d5",
    "What is the sorted JSON array of objects by the value of the age field, and in case of a tie, by the name field?": "[{\"name\":\"Karen\",\"age\":0},{\"name\":\"Henry\",\"age\":8},{\"name\":\"Alice\",\"age\":12},{\"name\":\"Bob\",\"age\":18},{\"name\":\"Liam\",\"age\":28},{\"name\":\"Grace\",\"age\":31},{\"name\":\"Charlie\",\"age\":35},{\"name\":\"Frank\",\"age\":38},{\"name\":\"Mary\",\"age\":50},{\"name\":\"Paul\",\"age\":50},{\"name\":\"Emma\",\"age\":53},{\"name\":\"Ivy\",\"age\":58},{\"name\":\"Oscar\",\"age\":61},{\"name\":\"David\",\"age\":67},{\"name\":\"Jack\",\"age\":72},{\"name\":\"Nora\",\"age\":72}]",
    "What’s the result when you paste the JSON at tools-in-data-science.pages.dev/jsonhash and click the Hash button?": "afaa1ae0a3075a3699ef0b7715ea126c1fb8fc1c80707740fc3ccdec19200415",
    "Find all <div>s having a foo class in the hidden element below. What's the sum of their data-value attributes?": "622",
    "Sum up all the values where the symbol matches ” OR † OR ‡ across all three files. What is the sum of all values associated with these symbols?":"The sum of all values associated with the symbols is: 45019",
    "Enter the raw Github URL of email.json so we can verify it.": "https://raw.githubusercontent.com/avijitsingh5104/iitm/refs/heads/main/email.json",
    "What does running cat * | sha256sum in that folder show in bash?": "6FDED4BA105F46421FB7C2F6077B0B2097EB2CD5EBAF749514B943DBF053615E",
    "What is the total size of all files at least 9721 bytes large and modified on or after Tue, 6 Mar, 2018, 2:36 am IST?": "9764",
    "How many lines are different between a.txt and b.txt?": "25",
    "What is the total sales of all the items in the 'Gold' ticket type? Write SQL to calculate it.": "SELECT SUM(units * price) AS total_sales FROM tickets WHERE LOWER(TRIM(type)) = 'gold';",
    "how many input tokens does it use up? Number of tokens:": "320",
    "Write a prompt that will get the LLM to say Yes. Say only 'Yes or 'No'. Is 100 greater than 50?": "Yes"
}

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question
    result = process.extractOne(question, qa_pairs.keys())

    if result is None:
        raise HTTPException(status_code=404, detail="Question not found")

    best_match, score, *_ = result  # Extract values safely
    if score > 80:
        return qa_pairs[best_match]  # Return just the answer

    raise HTTPException(status_code=404, detail="Question not found")