import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PhonePage } from './phone-page';

describe('PhonePage', () => {
  let component: PhonePage;
  let fixture: ComponentFixture<PhonePage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PhonePage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PhonePage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
