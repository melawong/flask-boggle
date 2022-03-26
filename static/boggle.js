"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();

  for(let row of board){
    $table.append($("<tr>"))

    for(let letter of row){
      const $td = $("<td>")
      $td.text(letter)
      $table.append($td)
    }
  }
}

start();

async function submitWord(evt){
  evt.preventDefault()

  const currentWord = $wordInput[0].value;
  const response = await axios.post("/api/score-word",
  {gameId, word : currentWord});
  handleWord(response.data.result, currentWord);

  $wordInput.val("");
}

$form.on("submit", submitWord)

async function handleWord(response, currentWord){

  switch(response){
    case "ok":
      $playedWords.append(`<li>${currentWord}</li>`)
      break;

    case "not-word":
      $message.empty()
      $message.text("Not a valid word!")
      break;

    case "not-on-board":
      $message.empty()
      $message.text("Not a playable word!")
      break;
  }

}