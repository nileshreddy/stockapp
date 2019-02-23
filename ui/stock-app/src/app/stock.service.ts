import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { Observable, of } from 'rxjs';
import { Stock } from './stock';



@Injectable({
  providedIn: 'root'
})
export class StockService {

  API_URL = "http://3.16.166.15:8080/";
  // API_URL = "http://localhost:8080/";
  constructor(private http: HttpClient) { }

  getTop10StocksData (): Observable<Stock[]> {
    let URL = this.API_URL+"gettop10stocks";
    return this.http.get<Stock[]>(URL).pipe(
      catchError(this.handleError('getTop10StocksData', []))
    );
  }

  searchStockNames(query:string): Observable<string[]> {
    let URL = this.API_URL+"searchStockNames?query="+query;
    return this.http.get<string[]>(URL).pipe(
      catchError(this.handleError('searchStockNames', []))
    );
  }

  getStockData(stockName:string): Observable<Stock> {
    let URL = this.API_URL+"getStockData?stockname="+stockName;
    return this.http.get<Stock>(URL).pipe(
      catchError(this.handleError('getStockData', null))
    );
  }


  /**
 * Handle Http operation that failed.
 * Let the app continue.
 * @param operation - name of the operation that failed
 * @param result - optional value to return as the observable result
 */
private handleError<T> (operation = 'operation', result?: T) {
  return (error: any): Observable<T> => {
 
    // TODO: send the error to remote logging infrastructure
    console.error(error); // log to console instead
 
    // TODO: better job of transforming error for user consumption
    // this.log(`${operation} failed: ${error.message}`);
 
    // Let the app keep running by returning an empty result.
    return of(result as T);
  };
}


}
