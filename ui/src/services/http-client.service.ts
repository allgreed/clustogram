export class HttpClientService {
    static get(url: string): Promise<Response> {
        return fetch(url)
    }
}
