export enum ArticleState {
    READ = 'READ',
    UNREAD = 'UNREAD'
}

interface ArticleOptions {
    title: string;
    content: string;
    link: string;
    id?: string;
    summary?: string;
    state: ArticleState;
    summaryTranslation?: string;
}

export interface ApiArticle {
    id: string;
    title: string;
    content: string;
    link: string;
    summary: string;
    state: ArticleState;
    summary_translation: string;
}

export const mapApiArticleToArticle = (apiArticle: ApiArticle): Article => {
    const newArticle = new Article(apiArticle);
    newArticle.summaryTranslation = apiArticle.summary_translation;
    return newArticle;
}

export class Article {
    id: string
    title: string;
    content: string;
    link: string;
    summary: string;
    state: ArticleState;
    summaryTranslation: string;

    constructor(options: ArticleOptions) {
        this.id = options.id || '';
        this.title = options.title;
        this.content = options.content;
        this.link = options.link;
        this.summary = options.summary || '';
        this.state = options.state;
        this.summaryTranslation = options.summaryTranslation || '';
    }

}