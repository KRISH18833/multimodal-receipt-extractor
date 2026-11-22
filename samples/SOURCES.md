# Sample Test Images Sources & Licenses

This directory contains test images for evaluating multimodal receipt extraction capabilities across different document types, handwriting, regional scripts, degradation, and non-document controls.

---

### 1. `test1.jpg`
- **Category**: Clear printed shop or restaurant receipt photo
- **Description**: Cash register receipt issued by a Swiss restaurant detailing items, prices, tax, and total.
- **Source Page**: [Wikimedia Commons: File:ReceiptSwiss.jpg](https://commons.wikimedia.org/wiki/File:ReceiptSwiss.jpg)
- **Direct URL**: `https://upload.wikimedia.org/wikipedia/commons/0/0b/ReceiptSwiss.jpg`
- **License**: [Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)](https://creativecommons.org/licenses/by-sa/3.0/)

---

### 2. `handwritten.jpg`
- **Category**: Handwritten bill or receipt photo
- **Description**: Historical handwritten receipt from Bull and Gate Inn, Macclesfield, recording line-item transactions, dates, and amounts in cursive handwriting.
- **Source Page**: [Wikimedia Commons: File:Macclesfield Receipt Bull and Gate Inn.jpg](https://commons.wikimedia.org/wiki/File:Macclesfield_Receipt_Bull_and_Gate_Inn.jpg)
- **Direct URL**: `https://upload.wikimedia.org/wikipedia/commons/9/97/Macclesfield_Receipt_Bull_and_Gate_Inn.jpg`
- **Author**: EnglishEnigma1
- **License**: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

---

### 3. `tamil_hindi.jpg`
- **Category**: Receipt or bill with Tamil or Hindi text
- **Description**: Government transport passenger receipt / bus ticket from Tamil Nadu, featuring printed Tamil script (`அரசு விரைவுப் போக்குவரத்துக் கழகம்`, `பயணச்சீட்டு எண்`), journey details, and fare amount.
- **Source Page**: [Wikimedia Commons: File:A bus ticket in Tamil Nadu.jpg](https://commons.wikimedia.org/wiki/File:A_bus_ticket_in_Tamil_Nadu.jpg)
- **Direct URL**: `https://upload.wikimedia.org/wikipedia/commons/9/97/A_bus_ticket_in_Tamil_Nadu.jpg`
- **Author**: Thamizhpparithi Maari
- **License**: [Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)](https://creativecommons.org/licenses/by-sa/3.0/)

---

### 4. `invoice.jpg`
- **Category**: Table-style company invoice
- **Description**: Merchandising proforma invoice structured in tabular columns (Description, Quantity, Unit Price, Total Amount).
- **Source Page**: [Wikimedia Commons: File:Performa invoice merchandising.jpg](https://commons.wikimedia.org/wiki/File:Performa_invoice_merchandising.jpg)
- **Direct URL**: `https://upload.wikimedia.org/wikipedia/commons/d/d8/Performa_invoice_merchandising.jpg`
- **License**: [Creative Commons CC0 1.0 Universal Public Domain Dedication (CC0 1.0)](https://creativecommons.org/publicdomain/zero/1.0/)

---

### 5. `non_receipt.jpg`
- **Category**: Non-document control image (landscape)
- **Description**: High-resolution mountain landscape photograph of Zagedan Lakes in the Caucasus Mountains, used to verify `document_type: not_a_document`.
- **Source Page**: [Wikimedia Commons: File:Zagedan Lakes, Mountain cirque, Caucasus Mountains.jpg](https://commons.wikimedia.org/wiki/File:Zagedan_Lakes,_Mountain_cirque,_Caucasus_Mountains.jpg)
- **Direct URL**: `https://upload.wikimedia.org/wikipedia/commons/8/88/Zagedan_Lakes%2C_Mountain_cirque%2C_Caucasus_Mountains.jpg`
- **License**: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

---

### 6. `blurry.jpg`
- **Category**: Degraded / blurry receipt image
- **Description**: Generated locally from `test1.jpg` using Pillow by applying `ImageFilter.GaussianBlur(radius=3)` and saving with JPEG quality 40 to evaluate model robustness and confidence scoring on poor quality images.
- **Source**: Synthetically generated from `samples/test1.jpg`.
- **License**: Derived under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).

---

### 7. `hard_blur.jpg`
- **Category**: Hard degraded receipt image (deliberate failure test case)
- **Description**: Generated locally from `test1.jpg` using Pillow by resizing to 40% of original dimensions, rotating 8 degrees with white fill (`expand=True`), applying `ImageFilter.GaussianBlur(radius=5)`, and saving with JPEG quality 25.
- **Source**: Derived from `samples/test1.jpg`.
- **License**: Derived under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).
