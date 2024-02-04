class Scraper {
    name: string;
    content: string;
    kwargs: string;

    constructor(name: string, content: string, kwargs: string) {
        this.name = name;
        this.content = content;
        this.kwargs = kwargs;
    }
}

export default Scraper;