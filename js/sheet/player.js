export class Player {
  constructor(data) {
    this.player = data.player;
    this.char = data.char;
    this.id = data.id;
    this.cla = data.cla;
    this.generation = data.generation;
    this.profilepicture = data.profilepicture;

    this.xp = data.xp;
    this.bloodpotency = data.bloodpotency;

    this.status = data.status;

    this.atributes = data.atributes;
    this.knowledges = data.knowledges;
    this.expertises = data.expertises;
    this.talents = data.talents;
    this.disciplines = data.disciplines;
    this.rituals = data.rituals;
    this.precedents = data.precedents;

    this.money = data.money;

    this.items = data.items;
    this.goals = data.goals;
    this.moralityes = data.moralityes;
    this.notes = data.notes;
    this.caracteristics = data.caracteristics;
  }
}