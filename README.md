Computação Visual e OCR
========

[![alt tag](https://codeclimate.com/github/ocr-doacao/cvocr/badges/gpa.svg)](https://codeclimate.com/github/ocr-doacao/cvocr)

Desenvolvimento de um sistema de tratamento de imagens baseado em opencv2 e tesseract.

Utilização
========

Algoritmo de fragmentação de imagem: python cv.py --help
 
Rodar ocr para todas as imagens de uma pasta: python ocr.py --help

Descobrir padrões nos resultados: python patterns.py --help

Rodar TUDO de uma única vez passando uma imagem e um diretório: python cvocr.py --help


Instalação
========

É necessário instalar as dependências de python (requirements.txt) e de sistema (requirements.system)

Estamos desenvolvendo um shell script para instalação automática: setup.sh

Seguem os códigos fonte e alguns tutoriais utilizados.

Código fonte do [tesseract](https://code.google.com/p/tesseract-ocr/downloads/detail?name=tesseract-ocr-3.02.02.tar.gz&can=2&q=)

Linguagem [português](https://code.google.com/p/tesseract-ocr/downloads/detail?name=tesseract-ocr-3.02.por.tar.gz&can=2&q=)

Diretório de downloads:

[fontes diversas](https://code.google.com/p/tesseract-ocr/downloads/list)

[git do tesseract](https://code.google.com/p/tesseract-ocr/source/checkout)

Dependências:

[leptonica](http://www.leptonica.org/download.html)


Links úteis:

[Instalando](https://code.google.com/p/tesseract-ocr/wiki/Compiling)

[Treinamento](https://code.google.com/p/tesseract-ocr/wiki/TrainingTesseract3)

Referências extras:

[Treinamento](http://www.win.tue.nl/~aeb/linux/ocr/tesseract.html)

Observações
========

O comando que roda todos os módulos de uma única vez apaga todos os arquivos do diretório!