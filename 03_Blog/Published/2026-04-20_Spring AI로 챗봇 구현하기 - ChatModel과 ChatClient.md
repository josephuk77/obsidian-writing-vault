---
title: "Spring AI로 챗봇 구현하기 - ChatModel과 ChatClient"
created: "2026-04-20"
type: blog
status: published
tags:
  - velog
publish_url: "https://velog.io/@josephuk77/Spring-AI로-챗봇-구현하기-ChatModel과-ChatClient"
---

# Spring AI로 챗봇 구현하기 - ChatModel과 ChatClient

이번에는 Spring AI를 이용해서 가장 기본적인 텍스트 챗봇을 구현하는 방법을 정리해보려고 한다.  
책에서는 먼저 간단하게 어떤 구현체와 함수들이 사용되는지 설명한 다음, ChatModel을 사용하는 방식으로 일반 응답과 스트리밍 응답을 구현하고, 마지막에 ChatClient를 이용한 더 간단한 방식까지 보여주는 흐름으로 설명하고 있었다. 나도 그 흐름대로 정리해봤다.

Spring AI로 챗봇을 만든다고 했을 때 전체적인 흐름은 생각보다 단순하다.  
프론트에서 질문을 보내면 컨트롤러가 요청을 받고, 서비스에서 Spring AI를 이용해 LLM에 질문을 전달한 뒤, 다시 응답을 받아 프론트에 내려주는 구조다.

전체 흐름을 간단하게 표현하면 아래와 같다.

```text
Frontend → Controller → Service → Spring AI → LLM → 응답 반환
```

---

# ChatModel과 ChatClient

Spring AI에서 텍스트 챗봇을 구현할 때 대표적으로 사용할 수 있는 방식은 두 가지다.

하나는 ChatModel을 직접 사용하는 방식이고, 다른 하나는 ChatClient를 사용하는 방식이다.

ChatModel은 조금 더 저수준 방식이라고 볼 수 있다.  
메시지 객체를 직접 만들고, Prompt를 직접 구성해서 모델을 호출한다. 그래서 내부 구조를 이해하기에는 더 좋다.

반대로 ChatClient는 ChatModel보다 더 편하게 사용할 수 있는 고수준 API다.  
prompt(), system(), user(), call() 같은 fluent API로 이어서 작성할 수 있어서 코드가 훨씬 짧아진다.

---

# 챗봇 구현에 사용되는 객체들

ChatModel 방식에서 사용되는 주요 객체는 다음과 같다.

- SystemMessage: 모델의 역할 정의
- UserMessage: 사용자 질문
- ChatOptions: 모델 설정
- Prompt: 전체 요청 객체
- ChatResponse: 모델 응답

---

# ChatModel을 사용한 일반 텍스트 응답

```java
public String generateText(String question) {
    SystemMessage systemMessage = SystemMessage.builder()
        .text("사용자 질문에 대해 한국어로 답변을 해야 합니다.")
        .build();

    UserMessage userMessage = UserMessage.builder()
        .text(question)
        .build();

    ChatOptions chatOptions = ChatOptions.builder()
        .model("gpt-4o-mini")
        .temperature(0.3)
        .maxTokens(1000)
        .build();

    Prompt prompt = Prompt.builder()
        .messages(systemMessage, userMessage)
        .chatOptions(chatOptions)
        .build();

    ChatResponse chatResponse = chatModel.call(prompt);
    AssistantMessage assistantMessage = chatResponse.getResult().getOutput();
    String answer = assistantMessage.getText();

    return answer;
}
```

이 흐름은 다음과 같다.

```text
SystemMessage 생성 → UserMessage 생성 → ChatOptions 설정 → Prompt 생성 → 모델 호출 → 응답 반환
```

---

# ChatModel을 사용한 스트리밍 응답

```java
public Flux<String> generateStreamText(String question) {
    SystemMessage systemMessage = SystemMessage.builder()
        .text("사용자 질문에 대해 한국어로 답변을 해야 합니다.")
        .build();

    UserMessage userMessage = UserMessage.builder()
        .text(question)
        .build();

    ChatOptions chatOptions = ChatOptions.builder()
        .model("gpt-4o")
        .temperature(0.3)
        .maxTokens(1000)
        .build();

    Prompt prompt = Prompt.builder()
        .messages(systemMessage, userMessage)
        .chatOptions(chatOptions)
        .build();

    Flux<ChatResponse> fluxResponse = chatModel.stream(prompt);

    Flux<String> fluxString = fluxResponse.map(chatResponse -> {
        AssistantMessage assistantMessage = chatResponse.getResult().getOutput();
        String chunk = assistantMessage.getText();
        if (chunk == null) chunk = "";
        return chunk;
    });

    return fluxString;
}
```

스트리밍 방식은 call() 대신 stream()을 사용하며, Flux 형태로 응답을 반환한다.

---

# Controller에서 요청 처리

```java
@PostMapping(
    value = "/chat-model",
    consumes = MediaType.APPLICATION_FORM_URLENCODED_VALUE,
    produces = MediaType.TEXT_PLAIN_VALUE
)
public String chatModel(@RequestParam("question") String question) {
    return aiService.generateText(question);
}
```

스트리밍 버전은 다음과 같다.

```java
@PostMapping(
    value = "/chat-model-stream",
    consumes = MediaType.APPLICATION_FORM_URLENCODED_VALUE,
    produces = MediaType.APPLICATION_NDJSON_VALUE
)
public Flux<String> chatModelStream(@RequestParam("question") String question) {
    return aiService.generateStreamText(question);
}
```

---

# 프론트에서 요청 보내기

```javascript
const response = await fetch('/ai/chat-model', {
  method: "post",
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/plain'
  },
  body: new URLSearchParams({ question })
});
```

---

# 스트리밍 응답 처리

```javascript
const reader = response.body.getReader();
const decoder = new TextDecoder("utf-8");
let content = "";

while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    let chunk = decoder.decode(value);
    content += chunk;

    const htmlContent = marked.parse(content);
    targetElement.innerHTML = htmlContent;
}
```

---

# ChatClient를 사용한 간단한 구현

```java
public String generateText(String question) {
    return chatClient.prompt()
        .system("사용자 질문에 대해 한국어로 답변을 해야 합니다.")
        .user(question)
        .options(ChatOptions.builder()
            .temperature(0.3)
            .maxTokens(1000)
            .build()
        )
        .call()
        .content();
}
```

스트리밍도 동일하게 간단하게 구현 가능하다.

```java
public Flux<String> generateStreamText(String question) {
    return chatClient.prompt()
        .system("사용자 질문에 대해 한국어로 답변을 해야 합니다.")
        .user(question)
        .options(ChatOptions.builder()
            .temperature(0.3)
            .maxTokens(1000)
            .build()
        )
        .stream()
        .content();
}
```

---

# 정리

Spring AI에서 챗봇의 핵심 흐름은 다음과 같다.

```text
질문 입력 → 메시지 구성 → Prompt 생성 → 모델 호출 → 응답 반환 → 화면 출력
```

ChatModel은 구조 이해에 좋고, ChatClient는 실제 구현에 더 편하다.

이 흐름을 이해하면 이후 Memory, RAG, Tool Calling 같은 기능을 붙이는 것도 훨씬 쉬워진다.
