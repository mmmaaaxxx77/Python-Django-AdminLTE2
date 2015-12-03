function User(data){
    this.username = data.username!=null?data.username:null;
    this.email = data.email!=null?data.email:null;
    this.last_login = data.last_login!=null?data.last_login:null;
    this.date_joined = data.date_joined!=null?data.date_joined:null;
    this.pictureId = data.pictureId!=null?data.pictureId:null;
}

function Group(data){
    this.name = data.name!=null?data.name:null;
}