service PingService {
    string ping(),
}
service AargsPingService {
    string ping(1:string ping);
}
service Sleep {
    oneway void sleep(1: i32 seconds)
}
