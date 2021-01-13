interface AppError {
    message: string
}

export class ErrorHandlerService {
    static handleError({ message }: AppError): void {
        console.error(message);
        alert(message);
    }
}
