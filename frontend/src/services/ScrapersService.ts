import axios from 'axios';
import Scraper from '@/models/Scraper';
import { ref, Ref } from 'vue';

class ScrapersService {
    private API_URL = 'http://127.0.0.1:5000/scrapers/scrapers';

    private ListScraper: Ref<Scraper[]> = ref([]);

    get listScraper(): Scraper[] {
        return this.ListScraper.value;
    }

    public async getScrapers(): Promise<Scraper[]> {
        const response = await axios.get<Scraper[]>(this.API_URL);
        this.ListScraper.value = response.data.reverse();
        return this.ListScraper.value;
    }

    public async runScraper(scraper: Scraper): Promise<void> {
        await axios.get<Scraper>(`${this.API_URL}/${scraper.name}/execute`);
    }

    public async addScraperByProperties(name: string, content: string, kwargs: string): Promise<void> {
        await this.addScraper(new Scraper(name, content, kwargs));
    }

    public async addScraper(scraper: Scraper): Promise<void> {
        await axios.post<Scraper>(this.API_URL, scraper);
        this.ListScraper.value.unshift(scraper);
    }

    public async deleteScraper(scraper: Scraper): Promise<void> {
        await axios.delete<Scraper>(`${this.API_URL}/${scraper.name}`);
        this.ListScraper.value = this.ListScraper.value.filter((s) => s.name !== scraper.name);
    }

    public async updateScraper(scraper: Scraper): Promise<void> {
        await axios.put<Scraper>(`${this.API_URL}/${scraper.name}`, scraper);
        this.ListScraper.value = this.ListScraper.value.map((s) => {
            if (s.name === scraper.name) {
                return scraper;
            }
            return s;
        });
    }
}

export default new ScrapersService();