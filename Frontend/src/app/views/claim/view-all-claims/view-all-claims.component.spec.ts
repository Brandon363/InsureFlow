import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewAllClaimsComponent } from './view-all-claims.component';

describe('ViewAllClaimsComponent', () => {
  let component: ViewAllClaimsComponent;
  let fixture: ComponentFixture<ViewAllClaimsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewAllClaimsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewAllClaimsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
