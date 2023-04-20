# Loads a PDF and perform queries on it

```
# Load the pdf into the model
http://localhost:5000/load?pdfFile=./pdfs/Atmel-8331-8-and-16-bit-AVR-Microcontroller-XMEGA-AU_Manual.pdf

# Ask questions on it
http://localhost:5000/query?k=25&query=how%20do%20the%20ADC%20works?
http://localhost:5000/query?k=25&query=steps%20to%20configure%20the%20ADC%20using%201%20channel
http://localhost:5000/query?k=25&query=describe%20ports%20related%20to%20the%20ADC
```
