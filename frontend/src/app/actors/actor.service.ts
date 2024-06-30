import { Injectable } from '@angular/core';
import { Observable, catchError, of, switchMap, tap } from 'rxjs';
import { Actor } from './actor';
import { MiddlewareService } from '../services/middleware.service';
import { HandleErrorService } from '../services/handleError.service';

@Injectable({ providedIn: 'root' })
export class ActorService extends HandleErrorService {
  constructor(private middlewareService: MiddlewareService) {
    super();
  }

  /** GET actors from the server */
  getActors(): Observable<Actor[]> {
    return this.middlewareService.get$<Actor[]>('actors').pipe(
      switchMap((response) => {
        const data = response?.data;
        let result;
        if (Array.isArray(data)) {
          result = data;
        } else {
          result = data ? [data] : [];
        }
        return of(result);
      }),
      tap((actors) => {
        console.log('fetched actors ', actors);
      }),
      catchError(this.handleError<Actor[]>('getActors', []))
    );
  }

  /** GET actor by id. Will 404 if id not found */
  getActor(id: number): Observable<Actor> {
    const url = `actors/${id}`;
    return this.middlewareService.get$<Actor>(url).pipe(
      switchMap((response) => of(response.data as Actor)),
      catchError(this.handleError<Actor>(`getActor id=${id}`))
    );
  }

  //////// Save methods //////////

  /** POST: add a new actor to the server */
  addActor(actor: Actor): Observable<Actor> {
    return this.middlewareService
      .post$<Actor, Actor>('actors', { data: actor })
      .pipe(
        switchMap((response) => of(response?.data as Actor)),
        tap((newActor: Actor) =>
          console.log(`added actor w/ id=${newActor.id}`)
        ),
        catchError(this.handleError<Actor>('addActor'))
      );
  }

  /** DELETE: delete the actor from the server */
  deleteActor(id: number): Observable<number> {
    const url = `actors/${id}`;

    return this.middlewareService
      .delete$<Actor, number>(url)
      .pipe(
        switchMap((response) => of(response?.data as number)),
        tap((_) => console.log(`deleted actor id=${id}`)),
        catchError(this.handleError<number>('deleteActor'))
      );
  }

  /** PUT: update the actor on the server */
  updateActor(actor: Actor): Observable<unknown> {
    const url = `actors/${actor.id}`;
    return this.middlewareService.patch$(url, {
      data: {
        name: actor.name,
        gender: actor.gender,
        age: actor.age,
      },
    }).pipe(
      switchMap((response) => of(response?.data)),
      tap((_) => console.log(`updated actor id=${actor.id}`)),
      catchError(this.handleError<unknown>('updateActor'))
    );
  }
}
