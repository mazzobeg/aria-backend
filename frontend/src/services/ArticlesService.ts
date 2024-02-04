import axios from 'axios';
import { ApiArticle, Article, ArticleState, mapApiArticleToArticle } from '@/models/Article';
import { ref, Ref } from 'vue';

class ArticlesService {
    private API_URL = 'http://127.0.0.1:5000/articles/articles';

    private ListArticle: Ref<Article[]> = ref([]);

    get listArticle(): Article[] {
        return this.ListArticle.value;
    }

    public async getArticles(): Promise<Article[]> {
        const response = await axios.get<ApiArticle[]>(this.API_URL);
        this.ListArticle.value = response.data.reverse().map(mapApiArticleToArticle);
        return this.ListArticle.value;
    }

    public async summarizeArticle(Article: Article): Promise<void> {
        await axios.get<Article>(`${this.API_URL}/${Article.id}/summarize`);
        await this.getArticles();
    }

    public async addArticleByProperties(title: string, content: string, link: string): Promise<void> {
        await this.addArticle(new Article({ title: title, content: content, link: link, state: ArticleState.UNREAD }));
    }

    public async addArticle(Article: Article): Promise<void> {
        await axios.post<Article>(this.API_URL, Article);
        this.ListArticle.value.unshift(Article);
    }

    public async deleteArticle(Article: Article): Promise<void> {
        await axios.delete<Article>(`${this.API_URL}/${Article.id}`);
        this.ListArticle.value = this.ListArticle.value.filter((s) => s.title !== Article.title);
    }

    public async updateArticle(Article: Article): Promise<void> {
        await axios.put<Article>(`${this.API_URL}/${Article.id}`, Article);
        this.ListArticle.value = this.ListArticle.value.map((s) => {
            if (s.id === Article.id) {
                return Article;
            }
            return s;
        });
    }

    public async markAsRead(Article: Article): Promise<void> {
        Article.state = ArticleState.READ;
        await this.updateArticle(Article);
        await this.getArticles();
    }

    public async markAsUnread(Article: Article): Promise<void> {
        Article.state = ArticleState.UNREAD;
        await this.updateArticle(Article);
        await this.getArticles();
    }

    public async switchState(Article: Article): Promise<void> {
        console.log("switchState", Article.state);
        if (Article.state === ArticleState.READ) {
            console.log("markAsUnread");
            await this.markAsUnread(Article);
        } else {
            await this.markAsRead(Article);
        }
    }

    public async translateArticle(Article: Article): Promise<void> {
        await axios.get<Article>(`${this.API_URL}/${Article.id}/translate`);
        await this.getArticles();
    }
}

export default new ArticlesService();