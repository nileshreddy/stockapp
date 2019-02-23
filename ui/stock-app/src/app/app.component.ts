import { Component, OnInit, ViewChild} from '@angular/core';
import { Stock } from './stock';
import { StockService } from './stock.service';

import {MatSort,MatTableDataSource} from '@angular/material';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{

  displayedColumns: string[] = ["code","name","open","high","low","close"];
  @ViewChild(MatSort) sort: MatSort;
  dataSource: MatTableDataSource<Stock>;

  stock: string;
  selectedStock: string;
  filteredStocks: string[];


  constructor(private stockservice:StockService){}

  ngOnInit() {
    this.getTop10Stocks();
    this.selectedStock = null;
    this.stock = null;
  }

  home(){
    this.getTop10Stocks();
    this.selectedStock = null;
    this.stock = null;
  }

  initTableData(tableData:Stock[]): void{
    this.dataSource = new MatTableDataSource<Stock>();
    this.dataSource.sort = this.sort;
    this.displayedColumns = this.displayedColumns;
    this.dataSource.data = tableData;
  }

  getTop10Stocks(){
    this.stockservice.getTop10StocksData()
    .subscribe((data: Stock[]) => {
      this.initTableData(data);
    });   
  }

  searchStocks(event) {
    let query = event.query;
    this.stockservice.searchStockNames(query).subscribe(stocks => {
        this.filteredStocks = stocks;
    });
  }

  selectStock(event){
    this.stockservice.getStockData(this.stock)
    .subscribe((data: Stock) => {
      let tableData :Stock[] = [];
      if(data){
        tableData = [data]
      }
      this.initTableData(tableData);
      this.selectedStock = this.stock;
    });   
  }


}
