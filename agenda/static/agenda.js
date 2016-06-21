var format = function (str, col) {
    col = typeof col === 'object' ? col : Array.prototype.slice.call(arguments, 1);

    return str.replace(/\{\{|\}\}|\{(\w+)\}/g, function (m, n) {
        if (m == "{{") { return "{"; }
        if (m == "}}") { return "}"; }
        return col[n];
    });
};

var dateToKey = function(date) {
	var year = date.getFullYear();
	var month = date.getMonth() + 1;
	var day = date.getDate();
	return format('{0}-{1}-{2}', year, month, day);
};

var getMonthUrl = function(date) {
	return format("/year/{0}/month/{1}", date.getFullYear(), date.getMonth()+1);
};

var app = {
	attachOnSave: function(onSaveHandler) {
		this.__onSaveHandler = onSaveHandler;
	},
	onSaveSuccess: function() {
		if(this.__onSaveHandler)
			this.__onSaveHandler();
	},
};

var Calendar = React.createClass({
	__onRecieveData: function(result) {
      	if (this.isMounted()) {
      		result.date = new Date(result.date);
        	this.setState(result);
      	}
	},
	
	__save: function(stamped) {
		var success = function(){
			$('#saved').fadeIn( "slow", function() {
			    $('#saved').fadeOut("slow");
			});
			app.onSaveSuccess();
		};
		$.post(
			'/save' + getMonthUrl(this.state.date), 
			{'stamped': JSON.stringify(stamped)}, 
			success, 
			'json'
		);
	},
	getInitialState: function() {
		var now = new Date();
        return {
            date: new Date(now.getFullYear(), now.getMonth(), now.getDate()),
            stamps: {},
            selectedStamp: null,
            stamped: {},
        };
    },
    componentDidMount: function() {
    	$.get(this.props.source, this.__onRecieveData);
    },
    handleDateChange: function(newDate) {
    	$.get(getMonthUrl(newDate), this.__onRecieveData);
  	},
  	handleStampSelect: function(stamp) {
    	this.setState({
    		selectedStamp: stamp,
    	});
  	},
  	handleStamp: function(date) {
  		if(!this.state.selectedStamp)
  			return;
  		var state = {'stamped': this.state.stamped};
  		var ids = this.state.stamped[dateToKey(date)] || [];
  		var index = ids.indexOf(this.state.selectedStamp.id);
  		if(index == -1)
  			ids.push(this.state.selectedStamp.id);
  		else
  			ids.splice(index, 1);
  		state.stamped[dateToKey(date)] = ids;
    	this.setState(state);
    	this.__save(state.stamped);
  	},
	render: function() {
		var days = [];
		var month = this.state.date.getMonth();
		var localDate = new Date(this.state.date);
		while(month == localDate.getMonth())
		{
			if(this.state.stamped[dateToKey(localDate)])
			{
				var stampIds = this.state.stamped[dateToKey(localDate)];
				var imgs = [];
				for(var i=0; i<stampIds.length; i++)
					imgs.push(this.state.stamps[stampIds[i]].img);
				days.push(<Day date={localDate} handleStamp={this.handleStamp} key={localDate.getTime()} imgs={imgs} />);
			}
			else
				days.push(<Day date={localDate} handleStamp={this.handleStamp} key={localDate.getTime()} />);
			localDate = new Date(localDate.getFullYear(), localDate.getMonth(), localDate.getDate()+1);
		}
		return (
			<div id="calendar">
				<YearPicker date={this.state.date} onDateChange={this.handleDateChange} handleNext={this.handleNext} />
				<div id="dayHeaders" >
					<div className="dayHeader">Mon</div>
					<div className="dayHeader">Tue</div>
					<div className="dayHeader">Wed</div>
					<div className="dayHeader">Thurs</div>
					<div className="dayHeader">Fri</div>
					<div className="dayHeader">Sat</div>
					<div className="dayHeader">Sun</div>
				</div>
				<StampPallet stamps={this.state.stamps} selectedStamp={this.state.selectedStamp} onStampSelect={this.handleStampSelect} />
				<div id="dayBoxes">
					{days}
				</div>
			</div>
		);
	}
});

var Day = React.createClass({
	WEEKDAYS: ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'],
	ROTATIONS: [-16, 5, 1, 15, -20, -1, -11, -21, -12, 11, 20, 17, -6, 14, 3, -19, 16, -9],
	handleStamp: function(event) {
		this.props.handleStamp(this.props.date);
	},
	render: function() {
		var imgNodes = [];
		if(this.props.imgs) {
			for(var i=0; i<this.props.imgs.length; i++) {
				var style = {
					transform: "rotate("+this.ROTATIONS[(this.props.date.getDate()+this.props.date.getMonth()+this.props.date.getYear()+i)%this.ROTATIONS.length]+"deg);",
				};
				imgNodes.push(<img className="dayStamp" style={style} src={this.props.imgs[i]} key={i} />);
			}
		}
		var classes = 'day '+this.WEEKDAYS[this.props.date.getDay()];
		var today = new Date();
		today.setHours(0, 0, 0, 0);
		if(this.props.date.getTime() === today.getTime())
			classes += ' today';
		return (
			<div className={classes} onClick={this.handleStamp}>
				{this.props.date.getDate()}
				<div id="dayStamps">{imgNodes}</div>
			</div>
		);
	}
});

var YearPicker = React.createClass({
	onDateChange: function(year, month, event) {
		var newDate = new Date(this.props.date.getFullYear()+year, this.props.date.getMonth()+month, 1);
		this.props.onDateChange(newDate);
	},
	render: function() {
		return (
			<div id="yearPicker">
				<button id="prevYear" onClick={this.onDateChange.bind(this, -1, 0)}>&lt;&lt;</button>
				<button id="prevMonth" onClick={this.onDateChange.bind(this, 0, -1)}>&lt;</button>
				<span className="date">{this.props.date.toLocaleString("en-us", { month: "long" })} {this.props.date.getFullYear()}</span>
				<button id="nextMonth" onClick={this.onDateChange.bind(this, 0, 1)}>&gt;</button>
				<button id="nextYear" onClick={this.onDateChange.bind(this, 1, 0)}>&gt;&gt;</button>
			</div>
		);
	}
});

var StampPallet = React.createClass({
	onStampSelect: function(stamp) {
		this.props.onStampSelect(stamp);
	},
	render: function() {
		var stamps = [];
		for(var key in this.props.stamps)
		{
			var classes = "stamp";
			if(this.props.selectedStamp && this.props.selectedStamp.name === this.props.stamps[key].name)
				classes += " selected";
			stamps.push(<img src={this.props.stamps[key].img} className={classes} onClick={this.onStampSelect.bind(this, this.props.stamps[key])} key={key} />);
		}
		return (
			<div id="stampPallet">
				<div>Stamps</div>
				{stamps}
				<pre className="notes">{"2X\n==\n30s\tPlank\n10x\tPress Up\n5x\tSquats\n10x\tSitup\n5x\tOverhead\n5x\tPull Up\n10x\tModified Bicycle\n6x\tBent Over Rows\n5x\tDeadlifts\n10x\tLateral Leg Raises\n10x\tBiceps Curls\n20x\tIron Cross"}</pre>
			</div>
		);
	}
});

var Streak = React.createClass({
	__load: function() {
		$.get(this.props.source, this.__onRecieveData);
	},
	__onRecieveData: function(result) {
      	if (this.isMounted()) {
      		this.setState(result);
      	}
	},
	getInitialState: function() {
		return {
            stamps: {},
            streak: [],
        };
    },
    componentDidMount: function() {
    	this.__load();
    	app.attachOnSave(this.__load);
    },
	render: function() {
		var streak = [];
		for(var i=0; i<this.state.streak.length; i++)
		{
			streak.push(<img key={i} className="streakStamp" src={this.state.streak[i].img} />);
		}
		return (
			<div id="streak">
				<div className="streakTitle">
                    Streak 
                    <span className="streakNum">({this.state.streak.length})</span>
                </div>
				{streak}
			</div>
		);
	}
});



React.render(
	<Calendar source={getMonthUrl(new Date())} ></Calendar>,
	document.getElementById('container')
);

React.render(
	<Streak source='/streak' ></Streak>,
	document.getElementById('streakContainer')
);