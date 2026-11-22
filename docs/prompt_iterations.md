# Prompt Iterations & Refinements

This document records the iteration history from `prompts/v1.txt` to `prompts/v2.txt`, detailing the prompt evolution and the rationale behind each prompt change.

---

## Prompt v1 (Initial Baseline)

```text
You are a document data extraction system. Look at the image and extract the data into the given schema.
- document_type must be one of: receipt, invoice, handwritten_bill, not_a_document
- date must be formatted YYYY-MM-DD if possible
- confidence values are between 0 and 1 for each field
- list any field you are unsure about in uncertain_fields
```

---

## Prompt v2 (Refined Production Prompt)

```text
You are a document data extraction system. Look at the image and extract the data into the given schema.

Rules:
- Return null for any field that is not clearly visible. Never guess or infer a value that is not printed or written on the document.
- document_type: one of receipt, invoice, handwritten_bill, not_a_document. Use not_a_document if the image is not a bill, receipt or invoice.
- merchant: the seller or business that issued the document, exactly as written, in the original script. Null if not shown.
- date: the date the document was issued or the transaction happened, formatted YYYY-MM-DD. Never use due dates, delivery dates or completion dates. If the date is only partly readable, return null and add "date" to uncertain_fields.
- currency: ISO code (INR, CHF, GBP, USD). If only a symbol or an old denomination is shown, give your best match and explain in notes.
- items: one entry per line item with name, qty and price as printed on that line.
- subtotal, tax, total: copy only if printed on the document. Never calculate them. total is the final amount payable.
- confidence: 0 to 1 per field. Use 0.0 for any field that is null. Use below 0.7 when the text is blurry, handwritten, cut off or ambiguous.
- uncertain_fields: list every field whose value you are not sure about, including any handwritten or blurry value.
- notes: at most 2 sentences. For non-English text, give an English translation of the merchant name. Mention odd currencies or anything ambiguous.
```

---

## What Changed and Why

- **Explicit rule to return `null` instead of guessing/calculating**: In v1, the model would invent or calculate missing totals (such as calculating `2919.0` on a blank invoice template), so v2 strictly mandates copying only printed values and returning `null` when not explicitly present.
- **Strict date definition avoiding completion/due dates**: In v1, `handwritten.jpg` had its transaction date falsely set to `1886-04-01` because the model picked up an agreed completion deadline rather than an issuance date, so v2 instructs never to use due, delivery, or completion dates.
- **English merchant translation in `notes`**: In v1, non-Latin scripts like Tamil on `tamil_hindi.jpg` were preserved in raw script with no transliteration or translation, so v2 requires providing an English translation of the merchant name in `notes`.
- **Zero confidence on `null` fields (`confidence: 0.0`)**: In v1, the model assigned confident scores like `1.0` to missing/null fields (e.g. `date: 1.0` and `subtotal: 1.0` on tickets without dates or subtotals), so v2 enforces `0.0` confidence for any field returning `null`.
- **Confidence threshold guidance for degraded text**: Added explicit instructions to set confidence `< 0.7` and register entries in `uncertain_fields` whenever documents feature cursive handwriting, blurriness, or truncation.
