// extract CSRF token from cookie
export function getCSRFToken() {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, 10) == ('csrftoken' + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

export function isAuthErrorStatusCode(statuscode: number) {
    return statuscode === 401 || statuscode === 403;
}

export function query4Text(el: Element, query: string): string {
    const found = el.querySelector(query);
    if (found && found.textContent) {
        return found.textContent
    }
    return ""
}
export function query4TextFromDoc(doc: Document, query: string): string {
    const found = doc.querySelector(query);
    if (found && found.textContent) {
        return found.textContent
    }
    return ""
}
export function queryExact(el: Element | Document, query: string): Element {
    const found = el.querySelector(query)
    if (!found) throw new Error(`element not found. query:${query}`)
    return found
}
export function getBindingClientRectSneaky(el: HTMLElement) {
    // not implemented.
    const disp = el.style.display
    el.style.display = 'block';
    const rect = el.getBoundingClientRect()
    el.style.display = disp
    return rect;
}