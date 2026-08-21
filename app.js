// =====================================================
// СПОРТИВНЫЙ АГЕНТ VK MINI APP V2
// =====================================================


// запуск VK Mini App

if (window.vkBridge) {

    vkBridge.send("VKWebAppInit")
    .then(() => {

        console.log("VK Mini App запущен");

    })
    .catch(error => {

        console.log(error);

    });

}
let currentQuestion = 0;


let child = {};
vkBridge.send("VKWebAppInit");



const API_URL = "https://sport-selector-ai-agent2.onrender.com/recommend";



// =====================================================
// Вопросы
// =====================================================


const questions = [


{
key:"gender",

title:"Пол ребенка",

type:"buttons",

answers:[
"👦 Мальчик",
"👧 Девочка"
]

},


{
key:"strength",

title:"Какая сила ребенка?",

answers:[
"Слабый",
"Средняя сила",
"Сильный"
]

},



{
key:"speed",

title:"Какая скорость реакции?",

answers:[
"Медленный",
"Средний",
"Быстрый"
]

},



{
key:"coordination",

title:"Как развита координация?",

answers:[
"Низкая",
"Средняя",
"Хорошая"
]

},



{
key:"endurance",

title:"Какая выносливость?",

answers:[
"Низкая",
"Средняя",
"Высокая"
]

},



{
key:"flexibility",

title:"Какая гибкость?",

answers:[
"Негибкий",
"Средняя",
"Гибкий"
]

},



{
key:"competition",

title:"Как относится к соревнованиям?",

answers:[
"Не любит",
"Иногда нравится",
"Любит побеждать"
]

},



{
key:"contact",

title:"Отношение к борьбе и контакту?",

answers:[
"Не любит контакт",
"Спокойно относится",
"Любит борьбу"
]

}

];



// =====================================================
// Старт
// =====================================================


function startTest(){


document.getElementById("app").innerHTML = `


<h2>
Данные ребенка
</h2>


<input id="age"
placeholder="Возраст">


<input id="height"
placeholder="Рост (см)">



<input id="weight"
placeholder="Вес (кг)">



<button onclick="saveInfo()">

Продолжить

</button>


`;

}




// =====================================================
// Сохранение данных
// =====================================================


function saveInfo(){



child.age =
document.getElementById("age").value;



child.height =
document.getElementById("height").value;



child.weight =
document.getElementById("weight").value;



if(
!child.age ||
!child.height ||
!child.weight
){

alert(
"Заполните все поля"
);

return;

}



currentQuestion = 0;


showQuestion();


}





// =====================================================
// Показ вопроса
// =====================================================


function showQuestion(){



let q =
questions[currentQuestion];



let progress =
Math.round(
((currentQuestion+1)
/questions.length)*100
);



let html = `


<h3>
Вопрос ${currentQuestion+1}
из ${questions.length}
</h3>



<div>

Прогресс:
${progress}%

</div>



<h2>
${q.title}
</h2>


`;



q.answers.forEach(answer=>{


html += `


<button class="option"

onclick="answer('${q.key}',
'${answer}')">

${answer}

</button>


`;


});



document.getElementById("app").innerHTML = html;



}




// =====================================================
// Ответ
// =====================================================


function answer(key,value){



child[key]=value;



currentQuestion++;



if(
currentQuestion >= questions.length
){

sendResult();

return;

}



showQuestion();


}




// =====================================================
// Отправка в API
// =====================================================


function sendResult(){



document.getElementById("app").innerHTML = `


<h2>
⏳ Анализируем данные...
</h2>


`;



fetch(

API_URL,

{

method:"POST",

headers:{

"Content-Type":
"application/json"

},


body:
JSON.stringify(child)

}

)



.then(async response=>{

    const text = await response.text();

    console.log("API RESPONSE:", text);

    return JSON.parse(text);

})


.then(data=>{


showResult(
data.result
);


})



.catch(error=>{


document.getElementById("app").innerHTML = `


<h2>
Ошибка соединения
</h2>


<p>
${error}
</p>


`;

});


}





// =====================================================
// Вывод результата
// =====================================================


function showResult(text){


document.getElementById("app").innerHTML = `


<h2>
🏆 Результа
</h2>


<div class="result">

${text.replace(/\n/g,"<br>")}

</div>



<button onclick="startTest()">

Пройти заново

</button>


`;

}