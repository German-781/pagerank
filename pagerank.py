import os
import random
from random import choice, sample

import re
import sys

DAMPING = 0.85
SAMPLES = 10000

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    salida = {}
    #paginas_factor = round((1.0 - damping_factor),5)
    paginas_factor = 1.0 - damping_factor

    largo = len(corpus)
 
    link = corpus[page]
    largolink = len(link)
    #pagina_factor = paginas_factor / largo

    pagina_factor = round((paginas_factor / (largo)),5)

    #link_factor = damping_factor / largolink
    link_factor = round((damping_factor / largolink),5)

    #pagina_sola = round(1 / largo,4)
    pagina_sola = 1 / largo

    for pagina in corpus:
        if link == None:
            salida[pagina] = pagina_sola
        else:
            if pagina in link:
                salida[pagina] = link_factor + pagina_factor
            else:
                salida[pagina] = pagina_factor

    return(salida)


    # raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample_PR = {}

    for page in corpus:
        sample_PR[page] = 0

    sample = None
    for iteration in range(n):
        if sample == None:
            # lista posibles elegibles
            choices = list(corpus.keys())       
            # elije una muestra al azar con igual probabilidad
            sample = random.choice(choices)
            sample_PR[sample] += 1
        else:
            # obtiene la probabilidad de distribución basado en la muestra actual
            prox_muestra_prob = transition_model(corpus, sample, damping_factor)
            # lista posibles elegibles
            choices = list(prox_muestra_prob.keys())
            #print("elegibles ", choices)
            # peso para elegiblesen lista de elegibles de salida de transition.model() para la muestra actual
            weights = [prox_muestra_prob[key] for key in choices]

            """""
             elije una muetra eligiendo al azar un elegible desde los elegibles
             con una probabilidad de distribucion definida, la selección al azar
             retorna una lista de valores, ya sea tomando el valor por uso del .pop(),
             o por el uso de index[0]
             """
            sample = random.choices(choices, weights).pop() 
            sample_PR[sample] += 1

    """""
        despues que el muestreo ha terminado, dividir los valores almacenados por
        el numero de iteraciones; para obtener el porcentaje
    """

    sample_PR = {key: round(value/n,4) for key, value in sample_PR.items()}

    return sample_PR

    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    n = SAMPLES
    
    salida = {}
    new_salida = {}

    paginas_factor = 1.0 - damping_factor

    largo = len(corpus)
 
    pagina_factor = round((paginas_factor / largo),4)

    pagina_sola = 1 / largo

    for pagina in corpus:
        salida[pagina] = pagina_sola

    for iteration in range(n):

        for pagina in corpus:

            link_rank = 0
            for pag in corpus:

                link_pag = corpus[pag]
                if pagina in link_pag:
                    pagina_rank = salida[pag]
                    num_link = len(link_pag) 
                    link_rank = round((link_rank + pagina_rank / num_link),4)

            pagina_link = round(damping_factor * link_rank,4)
            pagina_rank = round((pagina_factor + pagina_link),4)

            new_salida[pagina] = pagina_rank

        salida = new_salida
    return salida   
    
    #raise NotImplementedError


if __name__ == "__main__":
    main()
