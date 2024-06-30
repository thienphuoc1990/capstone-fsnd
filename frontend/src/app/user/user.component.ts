import { PageFlowService } from '../services/page-flow.service';
import { Component } from '@angular/core';
import { AuthService } from './auth.service';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-user',
  standalone: true,
  imports: [NgIf],
  templateUrl: './user.component.html',
  styleUrl: './user.component.scss',
})
export class UserComponent {
  loginURL!: string;
  constructor(
    public auth: AuthService,
    private pageFlowService: PageFlowService
  ) {
    this.loginURL = auth.build_login_link();
  }
}
