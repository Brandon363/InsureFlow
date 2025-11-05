import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FreeTextTestComponent } from './free-text-test.component';

describe('FreeTextTestComponent', () => {
  let component: FreeTextTestComponent;
  let fixture: ComponentFixture<FreeTextTestComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FreeTextTestComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FreeTextTestComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
