import { Component, OnInit } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../../environments/environment';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  private title = 'Hello first';

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    console.log('connecting to ' + environment.apiUrl);
    this.http.get(environment.apiUrl).subscribe({
        next: res => {
          // console.log(res);
          // this.title = 'Hello ' + res;
        },
        error: err => this.title = err
      });
  }

}
