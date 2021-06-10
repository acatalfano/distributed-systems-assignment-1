def generate_topic_domain(num_topics: int) -> list[str]:

    span: int = ord('z') - ord('a') + 1
    start: int = ord('a')
    result: list[str] = []
    for topic_index in range(num_topics):
        current_value: list[str] = []
        remainder: int = topic_index
        while True:
            current_value.append(chr(start + (remainder % span)))
            remainder //= span
            if remainder <= 0:
                break
        result.append(''.join(current_value))
    return result
