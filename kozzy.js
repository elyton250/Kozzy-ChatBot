async function sendMessage(){
    const input = document.getElementById('input');
    const repsonseDiv = document.getElementById('response');
    if (!input){
        ResponseDiv.innerHTML = 'Yes You Can Talk To Me';
        return;
    }
    responseDiv.innerHTML = 'loading...';
    try {
        const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
            method: "POST",
            headers: {
              "Authorization": "Bearer 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",
            //   "HTTP-Referer": "<YOUR_SITE_URL>", // Optional. Site URL for rankings on openrouter.ai.
            //   "X-Title": "<YOUR_SITE_NAME>", // Optional. Site title for rankings on openrouter.ai.
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              "model": "deepseek/deepseek-chat-v3-0324:free",
              "messages": [
                {
                  "role": "user",
                  "content": input
                }
              ]
            })
          });
          const data = response.json();
          const markdownText = 
            data.choices?.[0]?.message?.content || 'no response received';
            responseDiv.innerHTML = markdownText.parse(markdownText);
    } catch (error) {
        responseDiv.innerHTML = 'Sorry, I am not able to talk right now';
    }
}