"""generate_answer.py to generate the answer based on relevant information"""
import openai
import tools.credentials as credentials


def completion(information_relevant, prompt):
    """
    This function to generate answer based on relevant information using GPT-3.5-Turbo

    Args:
    information_relevant: The Information Retrieval result
    prompt: User's prompt

    Return:
    response: A response string from GPT-3.5-Turbo
    """

    system_prompt = f"""
    Anda adalah seorang dokter spesialis yang menjawab pertanyaan tentang obat, menstruasi, dan alergi.
    Jawablah pertanyaan dengan informasi di bawah ini. Jika pertanyaan tidak relevan, jawab dengan:
    "Mohon maaf. Saya tidak mengerti tentang pertanyaan anda, silahkan masukkan pertanyaan kembali dengan kalimat yang lebih sederhana."

    Informasi:
    {information_relevant}
    """
    
    full_prompt = f"{system_prompt}\n\nPertanyaan: {prompt}\nJawaban:"
    
    # Menggunakan model GPT-3.5 Turbo dengan chat-based format
    response = openai.ChatCompletion.create(
        model=credentials.DEPLOYMENT_CHAT,  # Gunakan model seperti 'gpt-3.5-turbo'
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0,
        stop=["\n", "Pertanyaan:"]
    )

    # Mengambil hasil jawaban dari response
    return response['choices'][0]['message']['content'].strip()
