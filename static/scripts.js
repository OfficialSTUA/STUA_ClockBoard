var data = null;
var delay = null;
var lirr = null;

var crit = [6, 9, 12, 12, 12, 25]

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function get_data() {
    let use_data = await fetch('http://206.189.183.69:7082/data').then(response => response.json());
    if (data == null) {
        data = JSON.parse(JSON.stringify(use_data));
        frame(document.getElementById("LHS_uptown_seventh_terminus_H1"), document.getElementById("LHS_uptown_seventh_terminus_DIV"), 0, 1.5, 0, "left_side.uptown_seventh.terminus", 0);
        frame(document.getElementById("LHS_downtown_seventh_terminus_H1"), document.getElementById("LHS_downtown_seventh_terminus_DIV"), 0, 1.5, 0, "left_side.downtown_seventh.terminus", 0);
        frame(document.getElementById("LHS_uptown_eighth_terminus_H1"), document.getElementById("LHS_uptown_eighth_terminus_DIV"), 0, 1.5, 0, "left_side.uptown_eighth.terminus", 0);
        frame(document.getElementById("LHS_downtown_eighth_terminus_H1"), document.getElementById("LHS_downtown_eighth_terminus_DIV"), 0, 1.5, 0, "left_side.downtown_eighth.terminus", 0);
        frame(document.getElementById("LHS_uptown_broadway_terminus_H1"), document.getElementById("LHS_uptown_broadway_terminus_DIV"), 0, 1.5, 0, "left_side.uptown_broadway.large.terminus", 0);
        frame(document.getElementById("RHS_downtown_broadway_terminus_H1"), document.getElementById("RHS_downtown_broadway_terminus_DIV"), 0, 1.5, 0, "right_side_standard.downtown_broadway.large.terminus", 0);
    } else {
        data = JSON.parse(JSON.stringify(use_data));
    }
    console.log(data);
    update_data();
}

async function get_delay() {
    delay = await fetch('http://206.189.183.69:7082/delay').then(response => response.json());
    //console.log(delay);
}

async function get_lirr() {
    lirr = await fetch('http://206.189.183.69:7082/lirr').then(response => response.json());
    //console.log(lirr);
}

// setInterval(get_delay, 30000)
// get_delay();

// setInterval(get_lirr, 30000)
// get_lirr();

setInterval(get_data, 30000)
get_data();

function update_data() {

    document.getElementById("LHS_uptown_seventh").innerHTML = data.data.left_side.uptown_seventh.emblem;
    document.getElementById("LHS_uptown_seventh_time").innerHTML = data.data.left_side.uptown_seventh.time;
    document.getElementById("LHS_downtown_seventh").innerHTML = data.data.left_side.downtown_seventh.emblem;
	document.getElementById("LHS_downtown_seventh_time").innerHTML = data.data.left_side.downtown_seventh.time;
    document.getElementById("LHS_uptown_eighth").innerHTML = data.data.left_side.uptown_eighth.emblem;
	document.getElementById("LHS_uptown_eighth_time").innerHTML = data.data.left_side.uptown_eighth.time;
    document.getElementById("LHS_downtown_eighth").innerHTML = data.data.left_side.downtown_eighth.emblem;
	document.getElementById("LHS_downtown_eighth_time").innerHTML = data.data.left_side.downtown_eighth.time;
    document.getElementById("RHS_downtown_broadway_large").innerHTML = data.data.right_side_standard.downtown_broadway.large.emblem;
	document.getElementById("RHS_downtown_broadway_large_time").innerHTML = data.data.right_side_standard.downtown_broadway.large.time;
    
    if (document.getElementById("LHS_uptown_seventh_time").innerHTML == `${crit[0]} minutes`) {
        document.getElementById("LHS_uptown_seventh").style.backgroundColor = "#111111";
        document.getElementById("LHS_uptown_seventh_time_DIV").style.backgroundColor = "#111111";
        document.getElementById("LHS_uptown_seventh_terminus_DIV").style.backgroundColor = "#111111";
        document.getElementById("LHS_uptown_seventh_time").classList.add("blink");
        document.getElementById("LHS_uptown_seventh_terminus_H1").classList.add("blink_terminus");
        document.getElementById("uptown7namediv").style.backgroundColor = "#111111";
        document.getElementById("uptown7name").style.color = "#ffffff";
    } else {
        document.getElementById("LHS_uptown_seventh").style.backgroundColor = "#e8e8e8";
        document.getElementById("LHS_uptown_seventh_time_DIV").style.backgroundColor = "#e8e8e8";
        document.getElementById("LHS_uptown_seventh_terminus_DIV").style.backgroundColor = "#e8e8e8";
        document.getElementById("LHS_uptown_seventh_time").classList.remove("blink");
        document.getElementById("LHS_uptown_seventh_terminus_H1").classList.remove("blink_terminus");
        document.getElementById("uptown7namediv").style.backgroundColor = "#e8e8e8";
        document.getElementById("uptown7name").style.color = "#000000";
    }
    if (document.getElementById("LHS_downtown_seventh_time").innerHTML == `${crit[0]} minutes`) {
        document.getElementById("LHS_downtown_seventh").style.backgroundColor = "#111111";
        document.getElementById("LHS_downtown_seventh_time_DIV").style.backgroundColor = "#111111";
        document.getElementById("LHS_downtown_seventh_terminus_DIV").style.backgroundColor = "#111111";
        document.getElementById("LHS_downtown_seventh_time").classList.add("blink");
        document.getElementById("LHS_downtown_seventh_terminus_H1").classList.add("blink_terminus");
        document.getElementById("downtown7namediv").style.backgroundColor = "#111111";
        document.getElementById("downtown7name").style.color = "#ffffff";
    } else {
        document.getElementById("LHS_downtown_seventh").style.backgroundColor = "#e8e8e8";
        document.getElementById("LHS_downtown_seventh_time_DIV").style.backgroundColor = "#e8e8e8";
        document.getElementById("LHS_downtown_seventh_terminus_DIV").style.backgroundColor = "#e8e8e8";
        document.getElementById("LHS_downtown_seventh_time").classList.remove("blink");
        document.getElementById("LHS_downtown_seventh_terminus_H1").classList.remove("blink_terminus");
        document.getElementById("downtown7namediv").style.backgroundColor = "#e8e8e8";
        document.getElementById("downtown7name").style.color = "#000000";
    }
    if (document.getElementById("LHS_uptown_eighth_time").innerHTML == `${crit[1]} minutes`) {
        document.getElementById("LHS_uptown_eighth").style.backgroundColor = "#111111";
        document.getElementById("LHS_uptown_eighth_time_DIV").style.backgroundColor = "#111111";
        document.getElementById("LHS_uptown_eighth_terminus_DIV").style.backgroundColor = "#111111";
        document.getElementById("LHS_uptown_eighth_time").classList.add("blink");
        document.getElementById("LHS_uptown_eighth_terminus_H1").classList.add("blink_terminus");
        document.getElementById("uptown8namediv").style.backgroundColor = "#111111";
        document.getElementById("uptown8name").style.color = "#ffffff";
    } else {
        document.getElementById("LHS_uptown_eighth").style.backgroundColor = "#e8e8e8";
        document.getElementById("LHS_uptown_eighth_time_DIV").style.backgroundColor = "#e8e8e8";
        document.getElementById("LHS_uptown_eighth_terminus_DIV").style.backgroundColor = "#e8e8e8";
        document.getElementById("LHS_uptown_eighth_time").classList.remove("blink");
        document.getElementById("LHS_uptown_eighth_terminus_H1").classList.remove("blink_terminus");
        document.getElementById("uptown8namediv").style.backgroundColor = "#e8e8e8";
        document.getElementById("uptown8name").style.color = "#000000";
    }
    if (document.getElementById("LHS_downtown_eighth_time").innerHTML == `${crit[1]} minutes`) {
        document.getElementById("LHS_downtown_eighth").style.backgroundColor = "#111111";
        document.getElementById("LHS_downtown_eighth_time_DIV").style.backgroundColor = "#111111";
        document.getElementById("LHS_downtown_eighth_terminus_DIV").style.backgroundColor = "#111111";
        document.getElementById("LHS_downtown_eighth_time").classList.add("blink");
        document.getElementById("LHS_downtown_eighth_terminus_H1").classList.add("blink_terminus");
        document.getElementById("downtown8namediv").style.backgroundColor = "#111111";
        document.getElementById("downtown8name").style.color = "#ffffff";
    } else {
        document.getElementById("LHS_downtown_eighth").style.backgroundColor = "#e8e8e8";
        document.getElementById("LHS_downtown_eighth_time_DIV").style.backgroundColor = "#e8e8e8";
        document.getElementById("LHS_downtown_eighth_terminus_DIV").style.backgroundColor = "#e8e8e8";
        document.getElementById("LHS_downtown_eighth_time").classList.remove("blink");
        document.getElementById("LHS_downtown_eighth_terminus_H1").classList.remove("blink_terminus");
        document.getElementById("downtown8namediv").style.backgroundColor = "#e8e8e8";
        document.getElementById("downtown8name").style.color = "#000000";
    }
    if (document.getElementById("RHS_downtown_broadway_large_time").innerHTML == `${crit[2]} minutes`) {
        document.getElementById("RHS_downtown_broadway_large").style.backgroundColor = "#222222";
        document.getElementById("RHS_downtown_broadway_time_DIV").style.backgroundColor = "#222222";
        document.getElementById("RHS_downtown_broadway_terminus_DIV").style.backgroundColor = "#222222";
        document.getElementById("RHS_downtown_broadway_large_time").classList.add("blink");
        document.getElementById("RHS_downtown_broadway_terminus_H1").classList.add("blink_terminus");
        document.getElementById("downtownbwaynamediv").style.backgroundColor = "#222222";
        document.getElementById("downtownbwayname").style.color = "#ffffff";
    } else {
        document.getElementById("RHS_downtown_broadway_time_DIV").style.backgroundColor = "#dddddd";
        document.getElementById("RHS_downtown_broadway_large").style.backgroundColor = "#dddddd";
        document.getElementById("RHS_downtown_broadway_terminus_DIV").style.backgroundColor = "#dddddd";
        document.getElementById("RHS_downtown_broadway_large_time").classList.remove("blink");
        document.getElementById("RHS_downtown_broadway_terminus_H1").classList.remove("blink_terminus");
        document.getElementById("downtownbwaynamediv").style.backgroundColor = "#dddddd";
        document.getElementById("downtownbwayname").style.color = "#000000";
    }

    document.getElementById("seventh_uptown_one").innerHTML = data.data.right_side_standard.uptown_seventh.one.emblem;
    document.getElementById("seventh_uptown_one_time").innerHTML = data.data.right_side_standard.uptown_seventh.one.time;
    if (data.data.right_side_standard.uptown_seventh.one.branch != null) {
        document.getElementById("seventh_uptown_one").innerHTML += `<h1 class="branch">${data.data.right_side_standard.uptown_seventh.one.branch}</h1>`;
    }
    document.getElementById("seventh_uptown_two").innerHTML = data.data.right_side_standard.uptown_seventh.two.emblem;
    document.getElementById("seventh_uptown_two_time").innerHTML = data.data.right_side_standard.uptown_seventh.two.time;
    if (data.data.right_side_standard.uptown_seventh.two.branch != null) {
        document.getElementById("seventh_uptown_two").innerHTML += `<h1 class="branch">${data.data.right_side_standard.uptown_seventh.two.branch}</h1>`;
    }
    document.getElementById("seventh_uptown_three").innerHTML = data.data.right_side_standard.uptown_seventh.three.emblem;
    document.getElementById("seventh_uptown_three_time").innerHTML = data.data.right_side_standard.uptown_seventh.three.time;
    if (data.data.right_side_standard.uptown_seventh.three.branch != null) {
        document.getElementById("seventh_uptown_three").innerHTML += `<h1 class="branch">${data.data.right_side_standard.uptown_seventh.three.branch}</h1>`;
    }
    document.getElementById("seventh_uptown_four").innerHTML = data.data.right_side_standard.uptown_seventh.four.emblem;
    document.getElementById("seventh_uptown_four_time").innerHTML = data.data.right_side_standard.uptown_seventh.four.time;
    if (data.data.right_side_standard.uptown_seventh.four.branch != null) {
        document.getElementById("seventh_uptown_four").innerHTML += `<h1 class="branch">${data.data.right_side_standard.uptown_seventh.four.branch}</h1>`;
    }
    document.getElementById("seventh_downtown_one").innerHTML = data.data.right_side_standard.downtown_seventh.one.emblem;
    document.getElementById("seventh_downtown_one_time").innerHTML = data.data.right_side_standard.downtown_seventh.one.time;
    if (data.data.right_side_standard.downtown_seventh.one.branch != null) {
        document.getElementById("seventh_downtown_one").innerHTML += `<h1 class="branch">${data.data.right_side_standard.downtown_seventh.one.branch}</h1>`;
    }
    document.getElementById("seventh_downtown_two").innerHTML = data.data.right_side_standard.downtown_seventh.two.emblem;
    document.getElementById("seventh_downtown_two_time").innerHTML = data.data.right_side_standard.downtown_seventh.two.time;
    if (data.data.right_side_standard.downtown_seventh.two.branch != null) {
        document.getElementById("seventh_downtown_two").innerHTML += `<h1 class="branch">${data.data.right_side_standard.downtown_seventh.two.branch}</h1>`;
    }
    document.getElementById("seventh_downtown_three").innerHTML = data.data.right_side_standard.downtown_seventh.three.emblem;
    document.getElementById("seventh_downtown_three_time").innerHTML = data.data.right_side_standard.downtown_seventh.three.time;
    if (data.data.right_side_standard.downtown_seventh.three.branch != null) {
        document.getElementById("seventh_downtown_three").innerHTML += `<h1 class="branch">${data.data.right_side_standard.downtown_seventh.three.branch}</h1>`;
    }
    document.getElementById("seventh_downtown_four").innerHTML = data.data.right_side_standard.downtown_seventh.four.emblem;
    document.getElementById("seventh_downtown_four_time").innerHTML = data.data.right_side_standard.downtown_seventh.four.time;
    if (data.data.right_side_standard.downtown_seventh.four.branch != null) {
        document.getElementById("seventh_downtown_four").innerHTML += `<h1 class="branch">${data.data.right_side_standard.downtown_seventh.four.branch}</h1>`;
    }
    document.getElementById("eighth_uptown_one").innerHTML = data.data.right_side_standard.uptown_eighth.one.emblem;
    document.getElementById("eighth_uptown_one_time").innerHTML = data.data.right_side_standard.uptown_eighth.one.time;
    if (data.data.right_side_standard.uptown_eighth.one.branch != null) {
        document.getElementById("eighth_uptown_one").innerHTML += `<h1 class="branch">${data.data.right_side_standard.uptown_eighth.one.branch}</h1>`;
    }
    document.getElementById("eighth_uptown_two").innerHTML = data.data.right_side_standard.uptown_eighth.two.emblem;
    document.getElementById("eighth_uptown_two_time").innerHTML = data.data.right_side_standard.uptown_eighth.two.time;
    if (data.data.right_side_standard.uptown_eighth.two.branch != null) {
        document.getElementById("eighth_uptown_two").innerHTML += `<h1 class="branch">${data.data.right_side_standard.uptown_eighth.two.branch}</h1>`;
    }
    document.getElementById("eighth_uptown_three").innerHTML = data.data.right_side_standard.uptown_eighth.three.emblem;
    document.getElementById("eighth_uptown_three_time").innerHTML = data.data.right_side_standard.uptown_eighth.three.time;
    if (data.data.right_side_standard.uptown_eighth.three.branch != null) {
        document.getElementById("eighth_uptown_three").innerHTML += `<h1 class="branch">${data.data.right_side_standard.uptown_eighth.three.branch}</h1>`;
    }
    document.getElementById("eighth_uptown_four").innerHTML = data.data.right_side_standard.uptown_eighth.four.emblem;
    document.getElementById("eighth_uptown_four_time").innerHTML = data.data.right_side_standard.uptown_eighth.four.time;
    if (data.data.right_side_standard.uptown_eighth.four.branch != null) {
        document.getElementById("eighth_uptown_four").innerHTML += `<h1 class="branch">${data.data.right_side_standard.uptown_eighth.four.branch}</h1>`;
    }
    document.getElementById("eighth_downtown_one").innerHTML = data.data.right_side_standard.downtown_eighth.one.emblem;
    document.getElementById("eighth_downtown_one_time").innerHTML = data.data.right_side_standard.downtown_eighth.one.time;

    if (data.data.right_side_standard.downtown_eighth.one.branch != null) {
        document.getElementById("eighth_downtown_one").innerHTML += `<h1 class="branch">${data.data.right_side_standard.downtown_eighth.one.branch}</h1>`;
        //console.log(document.getElementById("eighth_downtown_one").innerHTML)
    }
    document.getElementById("eighth_downtown_two").innerHTML = data.data.right_side_standard.downtown_eighth.two.emblem;
    document.getElementById("eighth_downtown_two_time").innerHTML = data.data.right_side_standard.downtown_eighth.two.time;
    if (data.data.right_side_standard.downtown_eighth.two.branch != null) {
        document.getElementById("eighth_downtown_two").innerHTML += `<h1 class="branch">${data.data.right_side_standard.downtown_eighth.two.branch}</h1>`;
        //console.log(document.getElementById("eighth_downtown_two").innerHTML)
    }
    document.getElementById("eighth_downtown_three").innerHTML = data.data.right_side_standard.downtown_eighth.three.emblem;
    document.getElementById("eighth_downtown_three_time").innerHTML = data.data.right_side_standard.downtown_eighth.three.time;
    if (data.data.right_side_standard.downtown_eighth.three.branch != null) {
        document.getElementById("eighth_downtown_three").innerHTML += `<h1 class="branch">${data.data.right_side_standard.downtown_eighth.three.branch}</h1>`;
        //console.log(document.getElementById("eighth_downtown_three").innerHTML)
    }
    document.getElementById("eighth_downtown_four").innerHTML = data.data.right_side_standard.downtown_eighth.four.emblem;
    document.getElementById("eighth_downtown_four_time").innerHTML = data.data.right_side_standard.downtown_eighth.four.time;
    if (data.data.right_side_standard.downtown_eighth.four.branch != null) {
        document.getElementById("eighth_downtown_four").innerHTML += `<h1 class="branch">${data.data.right_side_standard.downtown_eighth.four.branch}</h1>`;
        //console.log(document.getElementById("eighth_downtown_four").innerHTML)
    }

    document.getElementById("RHS_downtown_broadway_small").innerHTML = data.data.right_side_standard.downtown_broadway.small.emblem;
	document.getElementById("RHS_downtown_broadway_small_time").innerHTML = data.data.right_side_standard.downtown_broadway.small.time;
    if (data.data.right_side_standard.downtown_broadway.small.branch != null) {
        document.getElementById("RHS_downtown_broadway_small").innerHTML += `<h1 class="branch">${data.data.right_side_standard.downtown_broadway.small.branch}</h1>`;
        //console.log(document.getElementById("eighth_downtown_four").innerHTML)
    }

    document.getElementById("uptown_jamaica_one").innerHTML = data.data.bottom_side.uptown_nassau.one.emblem;
    document.getElementById("uptown_jamaica_one_time").innerHTML = data.data.bottom_side.uptown_nassau.one.time;
    document.getElementById("uptown_jamaica_two").innerHTML = data.data.bottom_side.uptown_nassau.two.emblem;
    document.getElementById("uptown_jamaica_two_time").innerHTML = data.data.bottom_side.uptown_nassau.two.time;

    document.getElementById("bus_one").innerHTML = data.data.bottom_side.bus.one.route;
    document.getElementById("bus_one_time").innerHTML = data.data.bottom_side.bus.one.time;
    document.getElementById("bus_two").innerHTML = data.data.bottom_side.bus.two.route;
    document.getElementById("bus_two_time").innerHTML = data.data.bottom_side.bus.two.time;
    document.getElementById("bus_three").innerHTML = data.data.bottom_side.bus.three.route;
    document.getElementById("bus_three_time").innerHTML = data.data.bottom_side.bus.three.time;
    document.getElementById("bus_four").innerHTML = data.data.bottom_side.bus.four.route;
    document.getElementById("bus_four_time").innerHTML = data.data.bottom_side.bus.four.time;
    document.getElementById("bus_five").innerHTML = data.data.bottom_side.bus.five.route;
    document.getElementById("bus_five_time").innerHTML = data.data.bottom_side.bus.five.time;
    document.getElementById("bus_six").innerHTML = data.data.bottom_side.bus.six.route;
    document.getElementById("bus_six_time").innerHTML = data.data.bottom_side.bus.six.time;

    document.getElementById("uptown_lex_one").innerHTML = data.data.bottom_side.uptown_lex.one.emblem;
    document.getElementById("uptown_lex_one_time").innerHTML = data.data.bottom_side.uptown_lex.one.time;
    document.getElementById("uptown_lex_two").innerHTML = data.data.bottom_side.uptown_lex.two.emblem;
    document.getElementById("uptown_lex_two_time").innerHTML = data.data.bottom_side.uptown_lex.two.time;
    document.getElementById("uptown_lex_three").innerHTML = data.data.bottom_side.uptown_lex.three.emblem;
    document.getElementById("uptown_lex_three_time").innerHTML = data.data.bottom_side.uptown_lex.three.time;
    document.getElementById("uptown_lex_four").innerHTML = data.data.bottom_side.uptown_lex.four.emblem;
    document.getElementById("uptown_lex_four_time").innerHTML = data.data.bottom_side.uptown_lex.four.time;
    document.getElementById("bus_seven").innerHTML = data.data.bottom_side.bus.seven.route;
    document.getElementById("bus_seven_time").innerHTML = data.data.bottom_side.bus.seven.time;
    document.getElementById("bus_eight").innerHTML = data.data.bottom_side.bus.eight.route;
    document.getElementById("bus_eight_time").innerHTML = data.data.bottom_side.bus.eight.time;
    document.getElementById("bus_nine").innerHTML = data.data.bottom_side.bus.nine.route;
    document.getElementById("bus_nine_time").innerHTML = data.data.bottom_side.bus.nine.time;
    document.getElementById("bus_ten").innerHTML = data.data.bottom_side.bus.ten.route;
    document.getElementById("bus_ten_time").innerHTML = data.data.bottom_side.bus.ten.time;

}

async function swap(elem, alt, num) {
	elem.innerHTML = eval(`data.data.${alt}`)[num];
    //elem.innerHTML = "East New York-Broadway Junction";
}

async function frame(elem, elemdiv, org, inc, pos, alt, num) {
	if (elem.clientWidth < elemdiv.clientWidth) {
		elem.style.left = 0 + 'px';
		await sleep(5000);
		await swap(elem, alt, num);
	} else if (pos <= -(elem.clientWidth-elemdiv.clientWidth)-20) {
		await sleep(2000);
		pos = org;
		await swap(elem, alt, num);
		
	} else {
		
		pos -= inc;
		elem.style.left = pos + 'px';

		if (pos == org - inc) {
			await sleep(2000);
		}
	}
	// num += 1;
	// if (num > 1) {
	// 	num = 0;
	// }
	requestAnimationFrame(() => {
		this.frame(elem, elemdiv, org, inc, pos, alt, num)
	})
}