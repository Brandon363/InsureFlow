import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateTemporaryLossApplicationApplicationComponent } from './create-temporary-loss-application-application.component';

describe('CreateTemporaryLossApplicationApplicationComponent', () => {
  let component: CreateTemporaryLossApplicationApplicationComponent;
  let fixture: ComponentFixture<CreateTemporaryLossApplicationApplicationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateTemporaryLossApplicationApplicationComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateTemporaryLossApplicationApplicationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
