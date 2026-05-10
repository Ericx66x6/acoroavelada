export class GameData {
  constructor(data) {
    this.xp_cost = data.xp_cost;

    this.disciplines = data.disciplines;
    this.rituals = data.rituals;
    this.precedents = data.precedents;

    this.bloodpotency = data.bloodpotency;
    this.bloodpotency_generation = data.bloodpotency_generation;

    this.maxvalue_generation = data.maxvalue_generation;

    this.atributes = data.atributes;

    this.knowledges = data.knowledges;
    this.expertises = data.expertises;
    this.talents = data.talents;
    this.caracteristics = data.caracteristics;
  }
}