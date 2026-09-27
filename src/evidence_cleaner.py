import re


class EvidenceCleaner:

    REMOVE_PATTERNS = [

        r"www\..*",

        r"UID:.*",

        r"IRDAI.*",

        r"Registered Office.*",

        r"Customer Care.*",

        r"Scan to.*",

        r"Introduction",

        r"Terms and conditions.*",

        r"licensed user agreement.*"

    ]

    def clean(
        self,
        text: str,
        max_length: int = 180
    ) -> str:

        if not text:
            return ""

        cleaned = text.replace("\n", " ")

        cleaned = re.sub(r"\s+", " ", cleaned)

        for pattern in self.REMOVE_PATTERNS:
            cleaned = re.sub(
                pattern,
                "",
                cleaned,
                flags=re.IGNORECASE
            )

        cleaned = cleaned.strip()

        sentences = re.split(
            r"(?<=[.!?]) +",
            cleaned
        )

        summary = ""

        for sentence in sentences:

            if len(sentence) < 20:
                continue

            summary += sentence + " "

            if len(summary) >= max_length:
                break

        if not summary:
            summary = cleaned[:max_length]

        return summary.strip()