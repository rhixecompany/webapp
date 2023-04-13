import React from "react";

const Footer = () => {
  return (
    <footer>
      <div className="text-center py-3">
        <p>
          {" "}
          Copyright &copy; {new Date().getFullYear()}{" "}
          <a href="https://rhixescans.tk/">Rhixescans</a>
        </p>
      </div>
    </footer>
  );
};

export default Footer;
