import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SharedModules } from './views/shared/shared_modules';
import { CameraComponent } from "./views/camera/camera.component";

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, SharedModules, CameraComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'Frontend';
}
